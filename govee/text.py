"""Text display modes: morse, flash, scroll, segment_map."""

from .colors import hsv_to_rgb
from .font import (WIDTH, HEIGHT, NUM_SEGMENTS, char_bitmap, char_columns,
                   MORSE, MORSE_DOT, MORSE_DASH, MORSE_ELEMENT_GAP,
                   MORSE_LETTER_GAP, MORSE_WORD_GAP)


def letter_color(ch):
    ch = ch.upper()
    if "A" <= ch <= "Z":
        return hsv_to_rgb((ord(ch) - ord("A")) * (360.0 / 26), 0.85, 1.0)
    if "0" <= ch <= "9":
        return hsv_to_rgb(200 + (ord(ch) - ord("0")) * 18, 0.85, 1.0)
    return hsv_to_rgb(40, 0.85, 1.0)


def render_char(ch, color, bg=0):
    bm = char_bitmap(ch)
    colors = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            colors.append(color if bm[r][c] else bg)
    return colors


def morse_frames(text, color=0xFFFFFF, speed=1.0):
    """Yield (color_int, hold_seconds) tuples for morse code flashing.

    Uses whole-lamp colorRgb. dot=0.3s, dash=0.9s, element gap=0.3s,
    letter gap=0.3s, word gap=0.7s. Speed scales all durations.
    """
    dot = MORSE_DOT / speed
    dash = MORSE_DASH / speed
    egap = MORSE_ELEMENT_GAP / speed
    lgap = MORSE_LETTER_GAP / speed
    wgap = MORSE_WORD_GAP / speed
    for ch in text.upper():
        code = MORSE.get(ch)
        if code is None or code == "/":
            yield (0, wgap)
            continue
        for elem in code:
            if elem == ".":
                yield (color, dot)
            else:
                yield (color, dash)
            yield (0, egap)
        yield (0, lgap)


def flash_frames(text, color=None, bg=0, blank=True):
    """Yield whole-lamp color ints — one color per letter, blank between."""
    if not text:
        while True:
            yield 0
    while True:
        for ch in text:
            c = color if color is not None else letter_color(ch)
            yield c
            if blank:
                yield 0


def color_frames(text, color=None, blank=True):
    """Alias for flash_frames — whole-lamp color per letter."""
    return flash_frames(text, color=color, blank=blank)


def segment_map_frames(text, color=None, bg=0, blank=True):
    """Yield 15-color segment lists using 3x5 font (experimental)."""
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
    while True:
        for ch in text:
            c = color if color is not None else letter_color(ch)
            yield render_char(ch, c, bg)
            if blank:
                yield [bg] * NUM_SEGMENTS


def _build_text_columns(text):
    cols = []
    for ch in text:
        cols.extend(char_columns(ch))
        cols.append([False] * HEIGHT)
    return cols


def scroll_frames(text, color=None, bg=0, width=WIDTH):
    """Yield 15-color segment lists scrolling text across the display."""
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
        return
    cols = _build_text_columns(text)
    pad = [[False] * HEIGHT for _ in range(2)]
    cols = pad + cols + pad
    char_colors = {}
    for ch in text:
        if ch not in char_colors:
            char_colors[ch] = color if color is not None else letter_color(ch)
    if len(cols) <= width:
        while True:
            yield render_char(text[0], char_colors.get(text[0], 0xFFFFFF), bg)
        return
    while True:
        for start in range(len(cols) - width + 1):
            window = cols[start:start + width]
            colors = []
            for r in range(HEIGHT):
                for c in range(width):
                    lit = window[c][r] if c < len(window) else False
                    colors.append(char_colors.get(text[0], 0xFFFFFF) if lit else bg)
            yield colors
