"""Display controller managing the 15-segment lamp."""

import sys
import time

from .client import GoveeClient
from .colors import int_to_rgb, quantize_frame
from .font import WIDTH, HEIGHT, NUM_SEGMENTS


class GoveeDisplay:
    """High-level controller for the Govee H6022 segment display."""

    def __init__(self, client=None, num_segments=NUM_SEGMENTS, auto_power=True,
                 max_colors=0):
        self.client = client or GoveeClient()
        self.num_segments = num_segments
        self.auto_power = auto_power
        self.max_colors = max_colors
        self._powered = False
        self._frame_count = 0
        self._last_frame = None

    def _ensure_power(self):
        if self.auto_power and not self._powered:
            self.client.set_power(True)
            self._powered = True
            if not self.client.dry_run:
                time.sleep(0.3)

    def _normalize(self, colors):
        colors = list(colors)
        if len(colors) < self.num_segments:
            colors = colors + [0] * (self.num_segments - len(colors))
        elif len(colors) > self.num_segments:
            colors = colors[:self.num_segments]
        return colors

    def _preview(self, colors):
        lines = []
        for row in range(HEIGHT):
            line = ""
            for col in range(WIDTH):
                idx = row * WIDTH + col
                cv = colors[idx]
                if cv == 0:
                    line += "\033[2m..\033[0m"
                else:
                    rr, gg, bb = int_to_rgb(cv)
                    line += f"\033[38;2;{rr};{gg};{bb}m##\033[0m"
            lines.append(line)
        sys.stdout.write("\n".join(lines) + "\n")
        sys.stdout.flush()

    def render(self, colors):
        """Render a frame (list of 15 RGB integers) to the lamp."""
        colors = self._normalize(colors)
        if self.max_colors > 0:
            colors = quantize_frame(colors, self.max_colors)
        if self.client.dry_run:
            self._preview(colors)
            self._frame_count += 1
            self._last_frame = list(colors)
            return
        self._ensure_power()
        if self._last_frame is None:
            self.client.set_segments(colors)
        else:
            changed = {}
            for i, color in enumerate(colors):
                if color != self._last_frame[i]:
                    changed.setdefault(int(color), []).append(i)
            if changed:
                self.client.set_segment_groups(changed)
        self._last_frame = list(colors)
        self._frame_count += 1

    def clear(self):
        """Turn all segments off."""
        if self.client.dry_run:
            self._preview([0] * self.num_segments)
            self._last_frame = [0] * self.num_segments
            return
        self.client.set_segments([0] * self.num_segments)
        self._last_frame = [0] * self.num_segments

    def brightness(self, value):
        """Set brightness (0-100)."""
        self.client.set_brightness(value)

    def set_color(self, rgb):
        """Set the whole lamp to a single color."""
        self._ensure_power()
        self.client.set_color(rgb)

    def render_color(self, color):
        """Set the whole lamp to a single color (uses colorRgb capability)."""
        if self.client.dry_run:
            frame = [int(color)] * self.num_segments
            self._preview(frame)
            self._frame_count += 1
            return
        if color == 0:
            self.client.set_color(0)
        else:
            self._ensure_power()
            self.client.set_color(int(color))
        self._frame_count += 1

    def run_color_frames(self, color_gen, duration=None, frame_interval=1.0,
                         on_stop_clear=True):
        """Run a generator of single color ints (whole-lamp color mode)."""
        start = time.monotonic()
        count = 0
        try:
            for color in color_gen:
                if duration is not None and (time.monotonic() - start) >= duration:
                    break
                self.render_color(color)
                count += 1
                time.sleep(frame_interval)
        except KeyboardInterrupt:
            pass
        finally:
            if on_stop_clear:
                self.render_color(0)
        return count

    def power_off(self):
        """Turn the lamp off."""
        self.client.set_power(False)
        self._powered = False

    def run_frames(self, frames, duration=None, frame_interval=0.6,
                   on_stop_clear=True):
        """Run a frame generator, pacing output to the rate limit.

        Args:
            frames: iterable yielding lists of 15 colors.
            duration: stop after this many seconds (None = run forever).
            frame_interval: seconds to hold each frame.
            on_stop_clear: clear the display when finished.
        """
        start = time.monotonic()
        count = 0
        try:
            for frame in frames:
                if duration is not None and (time.monotonic() - start) >= duration:
                    break
                self.render(frame)
                count += 1
                time.sleep(frame_interval)
        except KeyboardInterrupt:
            pass
        finally:
            if on_stop_clear:
                self.clear()
        return count
