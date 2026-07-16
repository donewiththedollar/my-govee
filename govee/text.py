"""Text rendering: flash and scroll modes for the 15-segment display.

The H6022 lamp has 15 segments arranged in a strip (not a grid), so
2D letter shapes are not directly visible. To make text readable:

- **Auto-color mode** (default): each letter gets a unique color based on
  its position in the alphabet, so B, T, C are visually distinct even
  though the segment pattern alone may not form a recognizable letter.
- **Pattern mode**: each letter also lights a distinct subset of segments
  (flattened from the 3x5 font), adding a second visual differentiator.
- **Solid mode** (--solid): lights ALL 15 segments in the letter's color
  for maximum visibility on a 1D strip.
"""

from .colors import hsv_to_rgb
from .font import WIDTH, HEIGHT, NUM_SEGMENTS, char_bitmap, char_columns


def letter_color(ch):
    """Assign a unique color to a character based on its identity.

    Letters A-Z map to hues spread across the spectrum.
    Digits 0-9 map to blue-violet hues.
    Other characters get a warm amber.
    """
    ch = ch.upper()
    if "A" <= ch <= "Z":
        idx = ord(ch) - ord("A")
        hue = idx * (360.0 / 26)
        return hsv_to_rgb(hue, 0.85, 1.0)
    if "0" <= ch <= "9":
        idx = ord(ch) - ord("0")
        hue = 200 + idx * 18
        return hsv_to_rgb(hue, 0.85, 1.0)
    return hsv_to_rgb(40, 0.85, 1.0)


def render_char(ch, color, bg=0):
    """Render a single character to a list of 15 segment colors."""
    bm = char_bitmap(ch)
    colors = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            colors.append(color if bm[r][c] else bg)
    return colors


def render_solid(ch, color, bg=0):
    """Render a character as all 15 segments lit in its color."""
    return [color] * NUM_SEGMENTS


def flash_frames(text, color=None, bg=0, blank=True, solid=False):
    """Yield frames that flash each character sequentially (loops forever).

    Args:
        text: string to display.
        color: fixed color for all letters, or None for auto-color per letter.
        bg: background (off) color, default 0 (black).
        blank: insert a blank frame between letters.
        solid: if True, light all 15 segments per letter (max visibility).
    """
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
    render_fn = render_solid if solid else render_char
    while True:
        for ch in text:
            c = color if color is not None else letter_color(ch)
            yield render_fn(ch, c, bg)
            if blank:
                yield [bg] * NUM_SEGMENTS


def _build_text_columns(text):
    cols = []
    for ch in text:
        cols.extend(char_columns(ch))
        cols.append([False] * HEIGHT)
    return cols


def scroll_frames(text, color=None, bg=0, width=WIDTH):
    """Yield frames that scroll text across the display (loops forever).

    Each letter gets its own color (auto-color) unless a fixed color is given.
    """
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
        return
    cols = _build_text_columns(text)
    pad = [[False] * HEIGHT for _ in range(2)]
    cols = pad + cols + pad
    if len(cols) <= width:
        while True:
            c = color if color is not None else letter_color(text[0])
            yield render_char(text[0], c, bg)
        return
    char_colors = {}
    for ch in text:
        if ch not in char_colors:
            char_colors[ch] = color if color is not None else letter_color(ch)
    while True:
        for start in range(len(cols) - width + 1):
            window = cols[start:start + width]
            colors = []
            for r in range(HEIGHT):
                for c in range(width):
                    lit = window[c][r] if c < len(window) else False
                    if lit:
                        col_idx = start + c
                        ch_idx = 0
                        running = 2
                        for ci, ch in enumerate(text):
                            if running <= col_idx < running + WIDTH + 1:
                                ch_idx = ci
                                break
                            running += WIDTH + 1
                        ch = text[ch_idx] if ch_idx < len(text) else text[0]
                        colors.append(char_colors.get(ch, color or 0xFFFFFF))
                    else:
                        colors.append(bg)
            yield colors
