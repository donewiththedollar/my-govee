"""Full animation library — 34 animations, each yields frames of 15 RGB ints."""

import math
import random

from .colors import hsv_to_rgb, lerp_color, rgb_to_int
from .font import NUM_SEGMENTS

OFF = 0x000000
N = NUM_SEGMENTS


def rainbow_chase(num_segments=N, color=None):
    while True:
        for off in range(num_segments):
            yield [hsv_to_rgb(((i + off) * 360.0 / num_segments) % 360) for i in range(num_segments)]


def color_wave(num_segments=N, color=0x0000FF):
    while True:
        for step in range(num_segments):
            yield [lerp_color(OFF, color, 0.5 + 0.5 * math.sin((i - step) * 2 * math.pi / num_segments))
                   for i in range(num_segments)]


def pulse(num_segments=N, color=0xFF0000):
    while True:
        for step in range(num_segments):
            t = 0.5 + 0.5 * math.sin(step * 2 * math.pi / num_segments)
            yield [lerp_color(OFF, color, t)] * num_segments


def fire_flicker(num_segments=N, color=0xFF4500):
    while True:
        yield [lerp_color(OFF, color, 0.35 + 0.65 * random.random()) if random.random() > 0.1
               else lerp_color(color, 0xFFFF00, 0.4) for _ in range(num_segments)]


def matrix_rain(num_segments=N, color=0x00FF41):
    drops = [random.randint(-num_segments, 0) for _ in range(num_segments)]
    while True:
        frame = [OFF] * num_segments
        for i in range(num_segments):
            for tail in range(5):
                idx = drops[i] - tail
                if 0 <= idx < num_segments:
                    frame[idx] = lerp_color(OFF, color, 1.0 - tail * 0.2)
            drops[i] += 1
            if drops[i] - 5 > num_segments:
                drops[i] = random.randint(-num_segments, 0)
        yield frame


def ocean_wave(num_segments=N, color=0x0077BE):
    while True:
        for step in range(num_segments):
            yield [lerp_color(0x001133, color, 0.5 + 0.5 * math.sin((i + step) * 2 * math.pi / (num_segments / 2.0)))
                   for i in range(num_segments)]


def aurora_chase(num_segments=N, color=0x00FF7F):
    while True:
        for off in range(num_segments):
            frame = []
            for i in range(num_segments):
                hue = ((i + off) * 24) % 360
                if 80 <= hue <= 200 or 280 <= hue <= 340:
                    frame.append(hsv_to_rgb(hue, 0.75, 0.9))
                else:
                    frame.append(OFF)
            yield frame


def lightning_flash(num_segments=N, color=0xFFFFFF):
    while True:
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        yield [OFF] * num_segments
        yield [color] * num_segments
        yield [color if random.random() < 0.6 else OFF for _ in range(num_segments)]
        yield [OFF] * num_segments
        yield [OFF] * num_segments
        yield [OFF] * num_segments


def heartbeat(num_segments=N, color=0xDC143C):
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


def chase(num_segments=N, color=0x00FF00):
    while True:
        for off in range(num_segments):
            frame = [OFF] * num_segments
            for tail in range(4):
                idx = (off - tail) % num_segments
                frame[idx] = lerp_color(OFF, color, 1.0 - tail * 0.25)
            yield frame


def breathe(num_segments=N, color=0x9B59B6):
    while True:
        for step in range(num_segments):
            t = 0.5 + 0.5 * math.sin(step * 2 * math.pi / num_segments)
            yield [lerp_color(OFF, color, t)] * num_segments


def color_cycle(num_segments=N, color=None):
    while True:
        for step in range(num_segments):
            hue = (step * 360.0 / num_segments) % 360
            yield [hsv_to_rgb(hue, 1.0, 1.0)] * num_segments


def twinkle(num_segments=N, color=0xFFFFFF):
    while True:
        yield [color if random.random() < 0.4 else OFF for _ in range(num_segments)]


def gradient_shift(num_segments=N, color=None):
    while True:
        for off in range(num_segments):
            yield [hsv_to_rgb(((i + off) * 360.0 / num_segments) % 360) for i in range(num_segments)]


def police(num_segments=N, color=None):
    red, blue = 0xFF0000, 0x0000FF
    half = num_segments // 2
    while True:
        yield [red] * half + [OFF] * (num_segments - half)
        yield [OFF] * num_segments
        yield [OFF] * half + [blue] * (num_segments - half)
        yield [OFF] * num_segments


def candle(num_segments=N, color=0xFFA500):
    while True:
        t = 0.7 + 0.3 * random.random()
        c = lerp_color(OFF, color, t)
        if random.random() < 0.15:
            c = lerp_color(c, 0xFFFF66, 0.4)
        yield [c] * num_segments


def strobe(num_segments=N, color=0xFFFFFF):
    while True:
        yield [color] * num_segments
        yield [OFF] * num_segments


def static_noise(num_segments=N, color=0xFFFFFF):
    while True:
        yield [color if random.random() < 0.5 else OFF for _ in range(num_segments)]


def sunrise(num_segments=N, color=0xFF8C00):
    steps = num_segments * 2
    while True:
        for step in range(steps):
            yield [lerp_color(OFF, color, step / float(steps - 1))] * num_segments
        for step in range(steps):
            yield [lerp_color(OFF, color, 1.0 - step / float(steps - 1))] * num_segments


def color_bounce(num_segments=N, color=0x00FFFF):
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


# === NEW CREATIVE ANIMATIONS ===

def bitcoin_orange_pulse(num_segments=N, color=0xF7931A):
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


def whale_swim(num_segments=N, color=None):
    deep_blue = 0x003366
    whale_color = 0xADD8E6
    pos = 0
    direction = 1
    while True:
        frame = [deep_blue] * num_segments
        for i in range(3):
            idx = pos + i
            if 0 <= idx < num_segments:
                frame[idx] = whale_color
        if pos - 1 >= 0:
            frame[pos - 1] = lerp_color(deep_blue, whale_color, 0.3)
        if pos + 3 < num_segments:
            frame[pos + 3] = lerp_color(deep_blue, whale_color, 0.3)
        if random.random() < 0.3:
            bubble_idx = random.randint(0, num_segments - 1)
            frame[bubble_idx] = lerp_color(deep_blue, 0xFFFFFF, 0.4)
        yield frame
        pos += direction
        if pos >= num_segments - 3:
            direction = -1
        elif pos <= 0:
            direction = 1


def goldfish(num_segments=N, color=None):
    gold = 0xFFD700
    orange = 0xFF8C00
    tank = 0x002233
    pos = random.randint(0, num_segments - 1)
    vel = 1
    while True:
        frame = [tank] * num_segments
        if 0 <= pos < num_segments:
            frame[pos] = gold
        if 0 <= pos + 1 < num_segments:
            frame[pos + 1] = orange
        if random.random() < 0.2:
            vel = -vel
        if random.random() < 0.1:
            vel = random.choice([-1, 1])
        pos += vel
        if pos < 0:
            pos = 0
            vel = 1
        elif pos >= num_segments - 1:
            pos = num_segments - 2
            vel = -1
        yield frame


def lava_lamp(num_segments=N, color=None):
    colors = [0xFF4500, 0xFF8C00, 0xFFD700, 0xFF1493, 0x9400D3]
    t = 0
    while True:
        frame = []
        for i in range(num_segments):
            phase = (i * 0.5 + t * 0.3) % len(colors)
            idx1 = int(phase) % len(colors)
            idx2 = (idx1 + 1) % len(colors)
            frac = phase - int(phase)
            wave = 0.5 + 0.5 * math.sin(i * 0.8 + t * 0.5)
            c = lerp_color(colors[idx1], colors[idx2], frac)
            c = lerp_color(OFF, c, 0.3 + 0.7 * wave)
            frame.append(c)
        yield frame
        t += 1


def neon_sunset(num_segments=N, color=None):
    pink = 0xFF1493
    orange = 0xFF8C00
    purple = 0x9400D3
    while True:
        for step in range(num_segments):
            t = step / float(num_segments)
            frame = []
            for i in range(num_segments):
                pos = (i + step) % num_segments / float(num_segments)
                if pos < 0.33:
                    c = lerp_color(pink, orange, pos * 3)
                elif pos < 0.66:
                    c = lerp_color(orange, purple, (pos - 0.33) * 3)
                else:
                    c = lerp_color(purple, pink, (pos - 0.66) * 3)
                frame.append(c)
            yield frame


def cyberpunk(num_segments=N, color=None):
    magenta = 0xFF00FF
    cyan = 0x00FFFF
    while True:
        for step in range(num_segments):
            frame = []
            for i in range(num_segments):
                if (i + step) % 4 < 2:
                    frame.append(magenta)
                else:
                    frame.append(cyan)
            yield frame


def underwater(num_segments=N, color=None):
    deep = 0x003344
    mid = 0x0066AA
    bubbles = [random.randint(0, num_segments - 1) for _ in range(3)]
    bubble_pos = [0.0, 0.0, 0.0]
    while True:
        frame = []
        for i in range(num_segments):
            base = lerp_color(deep, mid, 0.5 + 0.5 * math.sin(i * 0.5))
            frame.append(base)
        for b in range(3):
            bubble_pos[b] += 1
            if bubble_pos[b] >= num_segments:
                bubble_pos[b] = 0
                bubbles[b] = random.randint(0, num_segments - 1)
            idx = int(bubbles[b])
            if 0 <= idx < num_segments:
                frame[idx] = lerp_color(frame[idx], 0xFFFFFF, 0.5)
        yield frame


def galaxy(num_segments=N, color=None):
    deep = 0x0A0014
    while True:
        frame = []
        for i in range(num_segments):
            r = random.random()
            if r < 0.15:
                frame.append(0xFFFFFF)
            elif r < 0.25:
                frame.append(hsv_to_rgb(random.randint(240, 280), 0.6, 0.9))
            elif r < 0.35:
                frame.append(hsv_to_rgb(random.randint(200, 240), 0.5, 0.7))
            else:
                frame.append(deep)
        yield frame


def bitcoin_rain(num_segments=N, color=0xF7931A):
    drops = [random.randint(-num_segments, 0) for _ in range(num_segments)]
    while True:
        frame = [0x1A0A00] * num_segments
        for i in range(num_segments):
            for tail in range(4):
                idx = drops[i] - tail
                if 0 <= idx < num_segments:
                    frame[idx] = lerp_color(0x1A0A00, color, 1.0 - tail * 0.25)
            drops[i] += 1
            if drops[i] - 4 > num_segments:
                drops[i] = random.randint(-num_segments, 0)
        yield frame


def rocket(num_segments=N, color=None):
    flame_core = 0xFFFFFF
    flame_mid = 0xFFD700
    flame_tail = 0xFF4500
    smoke = 0x333333
    pos = num_segments
    while True:
        frame = [smoke if random.random() < 0.3 else OFF for _ in range(num_segments)]
        if pos >= 0:
            frame[min(pos, num_segments - 1)] = flame_core
        if pos + 1 < num_segments:
            frame[pos + 1] = flame_mid
        if pos + 2 < num_segments:
            frame[pos + 2] = flame_tail
        if pos + 3 < num_segments:
            frame[pos + 3] = lerp_color(flame_tail, OFF, 0.5)
        yield frame
        pos -= 1
        if pos < -4:
            pos = num_segments


def rainbow_waterfall(num_segments=N, color=None):
    while True:
        for step in range(num_segments):
            frame = []
            for i in range(num_segments):
                hue = ((i - step) * 360.0 / num_segments) % 360
                v = 0.5 + 0.5 * math.sin((i - step) * 0.5)
                frame.append(hsv_to_rgb(hue, 1.0, v))
            yield frame


def disco(num_segments=N, color=None):
    while True:
        yield [hsv_to_rgb(random.randint(0, 359), 1.0, 1.0) for _ in range(num_segments)]


def flame_core(num_segments=N, color=None):
    center = num_segments // 2
    while True:
        frame = []
        for i in range(num_segments):
            dist = abs(i - center)
            if dist == 0:
                c = 0xFFFFFF
            elif dist == 1:
                c = 0xFFD700
            elif dist == 2:
                c = 0xFF8C00
            elif dist == 3:
                c = 0xFF4500
            elif dist == 4:
                c = 0x8B0000
            else:
                c = OFF
            flicker = 0.8 + 0.2 * random.random()
            frame.append(lerp_color(OFF, c, flicker))
        yield frame


def ice_crystal(num_segments=N, color=None):
    ice = 0xB0E0E6
    white = 0xFFFFFF
    deep = 0x001830
    while True:
        for step in range(num_segments):
            frame = []
            for i in range(num_segments):
                phase = (i + step) % 6
                if phase == 0:
                    c = white
                elif phase == 3:
                    c = ice
                else:
                    c = deep
                wave = 0.5 + 0.5 * math.sin((i + step) * 0.8)
                frame.append(lerp_color(deep, c, wave))
            yield frame


def toxic_slime(num_segments=N, color=None):
    green = 0x39FF14
    purple = 0x8B008B
    dark = 0x0A1A0A
    drips = [random.randint(0, num_segments - 1) for _ in range(3)]
    drip_pos = [0.0, 0.0, 0.0]
    while True:
        frame = [dark] * num_segments
        for i in range(num_segments):
            base = lerp_color(dark, green, 0.2 + 0.2 * math.sin(i * 0.7))
            frame[i] = base
        for d in range(3):
            drip_pos[d] += 1
            if drip_pos[d] >= num_segments:
                drip_pos[d] = 0
                drips[d] = random.randint(0, num_segments - 1)
            idx = int(drip_pos[d])
            if 0 <= idx < num_segments:
                frame[idx] = green
            if 0 <= idx - 1 < num_segments:
                frame[idx - 1] = lerp_color(green, purple, 0.5)
        yield frame


ANIMATIONS = {
    "rainbow_chase": rainbow_chase, "rainbow": rainbow_chase,
    "color_wave": color_wave, "wave": color_wave,
    "pulse": pulse, "fire_flicker": fire_flicker, "fire": fire_flicker,
    "matrix_rain": matrix_rain, "matrix": matrix_rain,
    "ocean_wave": ocean_wave, "ocean": ocean_wave,
    "aurora_chase": aurora_chase, "aurora": aurora_chase,
    "lightning_flash": lightning_flash, "lightning": lightning_flash,
    "heartbeat": heartbeat, "chase": chase, "breathe": breathe,
    "color_cycle": color_cycle, "twinkle": twinkle,
    "gradient_shift": gradient_shift, "gradient": gradient_shift,
    "police": police, "candle": candle, "strobe": strobe,
    "static_noise": static_noise, "noise": static_noise,
    "sunrise": sunrise, "color_bounce": color_bounce, "bounce": color_bounce,
    "bitcoin_orange_pulse": bitcoin_orange_pulse,
    "whale_swim": whale_swim, "goldfish": goldfish,
    "lava_lamp": lava_lamp, "neon_sunset": neon_sunset,
    "cyberpunk": cyberpunk, "underwater": underwater,
    "galaxy": galaxy, "bitcoin_rain": bitcoin_rain,
    "rocket": rocket, "rainbow_waterfall": rainbow_waterfall,
    "disco": disco, "flame_core": flame_core,
    "ice_crystal": ice_crystal, "toxic_slime": toxic_slime,
}


def get_animation(name):
    name = name.lower()
    if name not in ANIMATIONS:
        available = ", ".join(sorted({fn.__name__ for fn in ANIMATIONS.values()}))
        raise ValueError(f"Unknown animation: {name}. Available: {available}")
    return ANIMATIONS[name]


def list_animations():
    return sorted({fn.__name__ for fn in ANIMATIONS.values()})
