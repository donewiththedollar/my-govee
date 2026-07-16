"""Text rendering: flash and scroll modes for the 3x5 segment grid."""

from .font import WIDTH, HEIGHT, NUM_SEGMENTS, char_bitmap, char_columns


def render_char(ch, color, bg=0):
    """Render a single character to a list of 15 segment colors."""
    bm = char_bitmap(ch)
    colors = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            colors.append(color if bm[r][c] else bg)
    return colors


def flash_frames(text, color, bg=0, blank=True):
    """Yield frames that flash each character sequentially (loops forever)."""
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
    while True:
        for ch in text:
            yield render_char(ch, color, bg)
            if blank:
                yield [bg] * NUM_SEGMENTS


def _build_text_columns(text):
    cols = []
    for ch in text:
        cols.extend(char_columns(ch))
        cols.append([False] * HEIGHT)
    return cols


def scroll_frames(text, color, bg=0, width=WIDTH):
    """Yield frames that scroll text horizontally across the grid (loops forever)."""
    if not text:
        while True:
            yield [bg] * NUM_SEGMENTS
        return
    cols = _build_text_columns(text)
    pad = [[False] * HEIGHT for _ in range(2)]
    cols = pad + cols + pad
    if len(cols) <= width:
        while True:
            yield render_char(text[0], color, bg)
        return
    while True:
        for start in range(len(cols) - width + 1):
            window = cols[start:start + width]
            colors = []
            for r in range(HEIGHT):
                for c in range(width):
                    lit = window[c][r] if c < len(window) else False
                    colors.append(color if lit else bg)
            yield colors
