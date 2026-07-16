"""Animated scene generators for the 15-segment display."""

import math
import random

from .colors import hsv_to_rgb, lerp_color
from .font import NUM_SEGMENTS

OFF = 0x000000


def rainbow_chase(num_segments=NUM_SEGMENTS, color=None):
    """Rainbow colors chasing along the segments."""
    while True:
        for offset in range(num_segments):
            frame = []
            for i in range(num_segments):
                hue = ((i + offset) * 360.0 / num_segments) % 360
                frame.append(hsv_to_rgb(hue, 1.0, 1.0))
            yield frame


def color_wave(num_segments=NUM_SEGMENTS, color=0x0000FF):
    """Sine wave of a single color flowing along the segments."""
    while True:
        for step in range(num_segments):
            frame = []
            for i in range(num_segments):
                t = 0.5 + 0.5 * math.sin((i - step) * 2 * math.pi / num_segments)
                frame.append(lerp_color(OFF, color, t))
            yield frame


def pulse(num_segments=NUM_SEGMENTS, color=0xFF0000):
    """Whole-display pulsing a single color."""
    while True:
        for step in range(num_segments):
            t = 0.5 + 0.5 * math.sin(step * 2 * math.pi / num_segments)
            c = lerp_color(OFF, color, t)
            yield [c] * num_segments


def fire_flicker(num_segments=NUM_SEGMENTS, color=0xFF4500):
    """Random fire-like flickering with orange/red/yellow tones."""
    while True:
        frame = []
        for i in range(num_segments):
            flicker = 0.35 + 0.65 * random.random()
            c = lerp_color(OFF, color, flicker)
            if random.random() < 0.3:
                c = lerp_color(c, 0xFFFF00, 0.3)
            frame.append(c)
        yield frame


def matrix_rain(num_segments=NUM_SEGMENTS, color=0x00FF41):
    """Matrix-style digital rain with trailing tails."""
    drops = [random.randint(-num_segments, 0) for _ in range(num_segments)]
    while True:
        frame = [OFF] * num_segments
        for i in range(num_segments):
            pos = drops[i]
            for tail in range(5):
                idx = pos - tail
                if 0 <= idx < num_segments:
                    intensity = 1.0 - tail * 0.2
                    frame[idx] = lerp_color(OFF, color, intensity)
            drops[i] += 1
            if drops[i] - 5 > num_segments:
                drops[i] = random.randint(-num_segments, 0)
        yield frame


def ocean_wave(num_segments=NUM_SEGMENTS, color=0x0077BE):
    """Calm ocean wave in blue tones."""
    while True:
        for step in range(num_segments):
            frame = []
            for i in range(num_segments):
                t = 0.5 + 0.5 * math.sin((i + step) * 2 * math.pi / (num_segments / 2.0))
                c = lerp_color(0x001133, color, t)
                frame.append(c)
            yield frame


def aurora_chase(num_segments=NUM_SEGMENTS, color=0x00FF7F):
    """Aurora borealis chase with green/purple/teal hues."""
    while True:
        for offset in range(num_segments):
            frame = []
            for i in range(num_segments):
                hue = ((i + offset) * 24) % 360
                if 80 <= hue <= 200 or 280 <= hue <= 340:
                    c = hsv_to_rgb(hue, 0.75, 0.9)
                else:
                    c = OFF
                frame.append(c)
            yield frame


def lightning_flash(num_segments=NUM_SEGMENTS, color=0xFFFFFF):
    """Lightning storm with random white flashes."""
    while True:
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        frame = [color if random.random() < 0.6 else OFF for _ in range(num_segments)]
        yield frame
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [OFF] * num_segments


def heartbeat(num_segments=NUM_SEGMENTS, color=0xDC143C):
    """Heartbeat rhythm: two quick pulses then rest."""
    while True:
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        yield [color] * num_segments
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [OFF] * num_segments


def chase(num_segments=NUM_SEGMENTS, color=0x00FF00):
    """Comet chase with a fading tail."""
    while True:
        for offset in range(num_segments):
            frame = [OFF] * num_segments
            for tail in range(4):
                idx = (offset - tail) % num_segments
                intensity = 1.0 - tail * 0.25
                frame[idx] = lerp_color(OFF, color, intensity)
            yield frame


def breathe(num_segments=NUM_SEGMENTS, color=0x9B59B6):
    """Slow breathing effect."""
    while True:
        for step in range(num_segments):
            t = 0.5 + 0.5 * math.sin(step * 2 * math.pi / num_segments)
            c = lerp_color(OFF, color, t)
            yield [c] * num_segments


def color_cycle(num_segments=NUM_SEGMENTS, color=None):
    """Cycle the whole display through the hue spectrum."""
    while True:
        for step in range(num_segments):
            hue = (step * 360.0 / num_segments) % 360
            c = hsv_to_rgb(hue, 1.0, 1.0)
            yield [c] * num_segments


def twinkle(num_segments=NUM_SEGMENTS, color=0xFFFFFF):
    """Random twinkling stars."""
    while True:
        frame = [color if random.random() < 0.4 else OFF for _ in range(num_segments)]
        yield frame


def gradient_shift(num_segments=NUM_SEGMENTS, color=None):
    """Shifting rainbow gradient."""
    while True:
        for offset in range(num_segments):
            frame = []
            for i in range(num_segments):
                hue = ((i + offset) * 360.0 / num_segments) % 360
                frame.append(hsv_to_rgb(hue, 1.0, 1.0))
            yield frame


def police(num_segments=NUM_SEGMENTS, color=None):
    """Alternating red and blue police lights."""
    red = 0xFF0000
    blue = 0x0000FF
    half = num_segments // 2
    while True:
        yield [red] * half + [OFF] * (num_segments - half)
        yield [OFF] * num_segments
        yield [OFF] * half + [blue] * (num_segments - half)
        yield [OFF] * num_segments


def candle(num_segments=NUM_SEGMENTS, color=0xFFA500):
    """Warm candle flicker."""
    while True:
        t = 0.7 + 0.3 * random.random()
        c = lerp_color(OFF, color, t)
        if random.random() < 0.15:
            c = lerp_color(c, 0xFFFF66, 0.4)
        yield [c] * num_segments


def strobe(num_segments=NUM_SEGMENTS, color=0xFFFFFF):
    """Fast strobe light."""
    while True:
        yield [color] * num_segments
        yield [OFF] * num_segments


def static_noise(num_segments=NUM_SEGMENTS, color=0xFFFFFF):
    """TV static / noise."""
    while True:
        yield [color if random.random() < 0.5 else OFF for _ in range(num_segments)]


def sunrise(num_segments=NUM_SEGMENTS, color=0xFF8C00):
    """Gradual sunrise from dark to warm orange."""
    steps = num_segments * 2
    while True:
        for step in range(steps):
            t = step / float(steps - 1)
            c = lerp_color(OFF, color, t)
            yield [c] * num_segments
        for step in range(steps):
            t = 1.0 - step / float(steps - 1)
            c = lerp_color(OFF, color, t)
            yield [c] * num_segments


def color_bounce(num_segments=NUM_SEGMENTS, color=0x00FFFF):
    """A ball of light bouncing back and forth."""
    while True:
        for pos in range(num_segments):
            frame = [OFF] * num_segments
            frame[pos] = color
            if pos > 0:
                frame[pos - 1] = lerp_color(OFF, color, 0.5)
            if pos < num_segments - 1:
                frame[pos + 1] = lerp_color(OFF, color, 0.5)
            yield frame
        for pos in range(num_segments - 1, -1, -1):
            frame = [OFF] * num_segments
            frame[pos] = color
            if pos > 0:
                frame[pos - 1] = lerp_color(OFF, color, 0.5)
            if pos < num_segments - 1:
                frame[pos + 1] = lerp_color(OFF, color, 0.5)
            yield frame


ANIMATIONS = {
    "rainbow": rainbow_chase,
    "rainbow_chase": rainbow_chase,
    "wave": color_wave,
    "color_wave": color_wave,
    "pulse": pulse,
    "fire": fire_flicker,
    "fire_flicker": fire_flicker,
    "matrix": matrix_rain,
    "matrix_rain": matrix_rain,
    "ocean": ocean_wave,
    "ocean_wave": ocean_wave,
    "aurora": aurora_chase,
    "aurora_chase": aurora_chase,
    "lightning": lightning_flash,
    "lightning_flash": lightning_flash,
    "heartbeat": heartbeat,
    "chase": chase,
    "breathe": breathe,
    "color_cycle": color_cycle,
    "twinkle": twinkle,
    "gradient": gradient_shift,
    "gradient_shift": gradient_shift,
    "police": police,
    "candle": candle,
    "strobe": strobe,
    "noise": static_noise,
    "static": static_noise,
    "sunrise": sunrise,
    "bounce": color_bounce,
    "color_bounce": color_bounce,
}


def get_animation(name):
    """Look up an animation function by name."""
    name = name.lower()
    if name not in ANIMATIONS:
        available = ", ".join(sorted({fn.__name__ for fn in ANIMATIONS.values()}))
        raise ValueError(f"Unknown animation: {name}. Available: {available}")
    return ANIMATIONS[name]


def list_animations():
    """Return sorted unique animation names."""
    return sorted({fn.__name__ for fn in ANIMATIONS.values()})
