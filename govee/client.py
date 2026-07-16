"""Govee Cloud API v2 client with rate limiting and retries."""

import json
import os
import threading
import time
import urllib.error
import urllib.request
import uuid

DEFAULT_BASE_URL = "https://openapi.api.govee.com/router/api/v1"
DEFAULT_SKU = "H6022"
RATE_LIMIT = 2.0
RATE_BURST = 6
HTTP_TIMEOUT = 15
MAX_RETRIES = 3
RETRY_STATUS = {429, 500, 502, 503, 504}


class GoveeConfigError(Exception):
    """Raised when required configuration (API key / device) is missing."""


class RateLimiter:
    """Token-bucket rate limiter (thread-safe)."""

    def __init__(self, rate=RATE_LIMIT, burst=RATE_BURST):
        self.rate = rate
        self.burst = burst
        self._tokens = float(burst)
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self):
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
            self._last = now
            if self._tokens < 1.0:
                wait = (1.0 - self._tokens) / self.rate
                time.sleep(wait)
                self._tokens = 0.0
                self._last = time.monotonic()
            else:
                self._tokens -= 1.0


class GoveeAPIError(Exception):
    """Raised when the Govee API returns an error."""


class GoveeClient:
    """Client for the Govee Cloud API v2."""

    def __init__(self, api_key=None, sku=None, device=None,
                 base_url=DEFAULT_BASE_URL, rate=RATE_LIMIT, burst=RATE_BURST,
                 dry_run=False):
        self.api_key = api_key or os.environ.get("GOVEE_API_KEY")
        self.sku = sku or os.environ.get("GOVEE_SKU") or DEFAULT_SKU
        self.device = device or os.environ.get("GOVEE_DEVICE")
        self.base_url = base_url.rstrip("/")
        self.dry_run = dry_run
        self._limiter = RateLimiter(rate, burst)
        if not self.dry_run:
            if not self.api_key:
                raise GoveeConfigError(
                    "Govee API key not found. Set the GOVEE_API_KEY environment "
                    "variable or pass --api-key. See README.md for setup."
                )
            if not self.device:
                raise GoveeConfigError(
                    "Govee device address not found. Set the GOVEE_DEVICE "
                    "environment variable or pass --device."
                )

    def _headers(self):
        return {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _request(self, path, payload):
        url = f"{self.base_url}{path}"
        body = json.dumps(payload).encode("utf-8")
        if self.dry_run:
            return {"code": 200, "message": "OK", "data": {}}
        self._limiter.acquire()
        last_error = None
        for attempt in range(MAX_RETRIES):
            req = urllib.request.Request(
                url, data=body, headers=self._headers(), method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                last_error = exc
                err_body = ""
                try:
                    err_body = exc.read().decode("utf-8", "replace")
                except Exception:
                    pass
                if exc.code in RETRY_STATUS and attempt < MAX_RETRIES - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise GoveeAPIError(f"HTTP {exc.code}: {err_body}") from exc
            except urllib.error.URLError as exc:
                last_error = exc
                if attempt < MAX_RETRIES - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise GoveeAPIError(f"Request failed: {exc}") from exc
        raise GoveeAPIError(f"Request failed after {MAX_RETRIES} retries: {last_error}")

    def _payload(self, commands=None, capability=None):
        payload = {
            "requestId": str(uuid.uuid4()),
            "payload": {
                "sku": self.sku,
                "device": self.device,
            },
        }
        if commands is not None:
            payload["payload"]["commands"] = commands
        if capability is not None:
            payload["payload"]["capability"] = capability
        return payload

    def control(self, commands):
        """Send one or more capability commands to the device."""
        if isinstance(commands, dict):
            commands = [commands]
        results = []
        for cap in commands:
            results.append(self._request("/device/control", self._payload(capability=cap)))
        return results[0] if len(results) == 1 else results

    def get_state(self, capability=None):
        """Query the device state."""
        return self._request("/device/state", self._payload(capability=capability))

    def set_power(self, on=True):
        """Turn the device on or off."""
        return self.control([{
            "type": "devices.capabilities.on_off",
            "instance": "powerSwitch",
            "value": 1 if on else 0,
        }])

    def set_brightness(self, value):
        """Set brightness (0-100)."""
        value = max(0, min(100, int(value)))
        return self.control([{
            "type": "devices.capabilities.range",
            "instance": "brightness",
            "value": value,
        }])

    def set_color(self, rgb):
        """Set the whole-lamp color."""
        return self.control([{
            "type": "devices.capabilities.color_setting",
            "instance": "colorRgb",
            "value": int(rgb),
        }])

    def set_segments(self, segment_colors, max_commands=0):
        """Set per-segment colors, grouping segments by color to minimize commands."""
        groups = {}
        for idx, color in enumerate(segment_colors):
            groups.setdefault(int(color), []).append(idx)
        commands = []
        for color, segments in groups.items():
            commands.append({
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {"segment": segments, "rgb": color},
            })
        if max_commands and len(commands) > max_commands:
            results = []
            for i in range(0, len(commands), max_commands):
                results.append(self.control(commands[i:i + max_commands]))
            return results
        return self.control(commands)

    def set_diy_scene(self, scene_code):
        """Activate a DIY scene."""
        return self.control([{
            "type": "devices.capabilities.dynamic_scene",
            "instance": "diyScene",
            "value": scene_code,
        }])

    def set_light_scene(self, scene_code):
        """Activate a preset light scene."""
        return self.control([{
            "type": "devices.capabilities.dynamic_scene",
            "instance": "lightScene",
            "value": scene_code,
        }])

    def set_snapshot(self, data):
        """Activate snapshot mode."""
        return self.control([{
            "type": "devices.capabilities.dynamic_scene",
            "instance": "snapshot",
            "value": data,
        }])
