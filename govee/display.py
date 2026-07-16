"""Display controller — manages the 15-segment lamp with signal-safe cleanup."""

import signal
import sys
import time

from .client import GoveeClient
from .colors import int_to_rgb, quantize_frame
from .font import WIDTH, HEIGHT, NUM_SEGMENTS

DEFAULT_DURATION = 10.0


class GoveeDisplay:
    def __init__(self, client=None, num_segments=NUM_SEGMENTS, auto_power=True,
                 max_colors=0):
        self.client = client or GoveeClient()
        self.num_segments = num_segments
        self.auto_power = auto_power
        self.max_colors = max_colors
        self._powered = False
        self._frame_count = 0
        self._last_frame = None
        self._stop = False

    def _ensure_power(self):
        if self.auto_power and not self._powered:
            self.client.set_power(True)
            self._powered = True
            if not self.client.dry_run:
                time.sleep(0.3)

    def _normalize(self, colors):
        colors = list(colors)
        if len(colors) < self.num_segments:
            colors += [0] * (self.num_segments - len(colors))
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

    def _install_signals(self):
        self._stop = False
        def _h(signum, frame):
            self._stop = True
        self._old_int = signal.signal(signal.SIGINT, _h)
        self._old_term = signal.signal(signal.SIGTERM, _h)

    def _restore_signals(self):
        signal.signal(signal.SIGINT, self._old_int)
        signal.signal(signal.SIGTERM, self._old_term)

    def render(self, colors):
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
            for i, c in enumerate(colors):
                if c != self._last_frame[i]:
                    changed.setdefault(int(c), []).append(i)
            if changed:
                self.client.set_segment_groups(changed)
        self._last_frame = list(colors)
        self._frame_count += 1

    def render_color(self, color):
        if self.client.dry_run:
            self._preview([int(color)] * self.num_segments)
            self._frame_count += 1
            return
        if color == 0:
            self.client.set_color(0)
        else:
            self._ensure_power()
            self.client.set_color(int(color))
        self._frame_count += 1

    def clear(self):
        if self.client.dry_run:
            self._preview([0] * self.num_segments)
            self._last_frame = [0] * self.num_segments
            return
        self.client.set_segments([0] * self.num_segments)
        self._last_frame = [0] * self.num_segments

    def brightness(self, value):
        self.client.set_brightness(value)

    def set_color(self, rgb):
        self._ensure_power()
        self.client.set_color(rgb)

    def power_off(self):
        self.client.set_power(False)
        self._powered = False

    def run_frames(self, frames, duration=DEFAULT_DURATION, frame_interval=0.6,
                   on_stop_clear=False):
        self._install_signals()
        start = time.monotonic()
        count = 0
        try:
            for frame in frames:
                if self._stop:
                    break
                if duration is not None and (time.monotonic() - start) >= duration:
                    break
                self.render(frame)
                count += 1
                time.sleep(frame_interval)
        except Exception:
            pass
        finally:
            self._restore_signals()
            if on_stop_clear:
                self.clear()
        return count

    def run_color_frames(self, color_gen, duration=DEFAULT_DURATION,
                         frame_interval=1.0, on_stop_clear=False):
        self._install_signals()
        start = time.monotonic()
        count = 0
        try:
            for color in color_gen:
                if self._stop:
                    break
                if duration is not None and (time.monotonic() - start) >= duration:
                    break
                self.render_color(color)
                count += 1
                time.sleep(frame_interval)
        except Exception:
            pass
        finally:
            self._restore_signals()
            if on_stop_clear:
                self.render_color(0)
        return count

    def run_timed_color_frames(self, timed_gen, duration=DEFAULT_DURATION,
                               on_stop_clear=False):
        """Run (color, hold_seconds) pairs — for morse code."""
        self._install_signals()
        start = time.monotonic()
        count = 0
        try:
            for color, hold in timed_gen:
                if self._stop:
                    break
                if duration is not None and (time.monotonic() - start) >= duration:
                    break
                self.render_color(color)
                count += 1
                if hold > 0:
                    time.sleep(hold)
        except Exception:
            pass
        finally:
            self._restore_signals()
            if on_stop_clear:
                self.render_color(0)
        return count

    def run_scene(self, scene, brightness=None, keep=False):
        """Run a scene with multiple steps (text + animation)."""
        self._install_signals()
        if brightness is not None:
            self.brightness(brightness)
        else:
            self.brightness(scene.get("brightness", 80))
        from . import text as text_mod
        from . import animations as anim_mod
        from .colors import parse_color
        total = 0
        try:
            for step in scene["steps"]:
                if self._stop:
                    break
                step_dur = step.get("duration", 5)
                if time.monotonic() - (start := time.monotonic()) > 0 and total > 100:
                    break
                if step["type"] == "text":
                    color = parse_color(step.get("color", "white"))
                    mode = step.get("mode", "morse")
                    txt = step.get("text", "").upper()
                    if mode == "morse":
                        gen = text_mod.morse_frames(txt, color=color)
                        n = self.run_timed_color_frames(gen, duration=step_dur)
                    elif mode == "flash":
                        gen = text_mod.flash_frames(txt, color=color)
                        n = self.run_color_frames(gen, duration=step_dur, frame_interval=1.0)
                    else:
                        gen = text_mod.segment_map_frames(txt, color=color)
                        n = self.run_frames(gen, duration=step_dur, frame_interval=0.8)
                    total += n
                elif step["type"] == "animate":
                    anim_fn = anim_mod.get_animation(step["name"])
                    frames = anim_fn()
                    n = self.run_frames(frames, duration=step_dur, frame_interval=0.6)
                    total += n
        except Exception:
            pass
        finally:
            self._restore_signals()
            if not keep:
                self.clear()
        return total
