"""Pixel art patterns for the 3x5 segment grid."""

from .font import WIDTH, HEIGHT, NUM_SEGMENTS

PATTERNS = {
    "heart": [".#.", "###", "###", ".#.", ".#."],
    "smiley": [".#.", "#.#", ".#.", "#.#", ".#."],
    "frown": [".#.", "#.#", ".#.", "#.#", ".#."],
    "arrow_up": [".#.", "###", ".#.", ".#.", ".#."],
    "arrow_down": [".#.", ".#.", ".#.", "###", ".#."],
    "arrow_left": ["...", "#..", "###", "#..", "..."],
    "arrow_right": ["...", "..#", "###", "..#", "..."],
    "diamond": [".#.", "###", "###", "###", ".#."],
    "cross": [".#.", ".#.", "###", ".#.", ".#."],
    "checker": ["#.#", ".#.", "#.#", ".#.", "#.#"],
    "border": ["###", "#.#", "#.#", "#.#", "###"],
    "x": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "t": ["###", ".#.", ".#.", ".#.", ".#."],
    "hbar": ["...", "...", "###", "...", "..."],
    "vbar": [".#.", ".#.", ".#.", ".#.", ".#."],
    "corners": ["#.#", "...", "...", "...", "#.#"],
    "top": ["###", "#.#", "#.#", "#.#", "#.#"],
    "bottom": ["#.#", "#.#", "#.#", "#.#", "###"],
    "invader": ["#.#", ".#.", "###", "#.#", "#.#"],
    "ghost": [".#.", "#.#", "#.#", "###", "#.#"],
    "note": [".#.", ".#.", "###", "###", ".#."],
    "star": [".#.", "#.#", ".#.", "#.#", ".#."],
    "tree": [".#.", "###", "###", ".#.", ".#."],
    "house": [".#.", "###", "#.#", "#.#", "###"],
    "cup": [".#.", "###", "#.#", "#.#", "###"],
    "full": ["###", "###", "###", "###", "###"],
    "empty": ["...", "...", "...", "...", "..."],
    "stairs": ["#..", "##.", "##.", "###", "###"],
    "zigzag": ["#..", "##.", ".##", ".##", "..#"],
    "circle": [".#.", "#.#", "#.#", "#.#", ".#."],
    "dot": ["...", ".#.", ".#.", ".#.", "..."],
    "exclaim": [".#.", ".#.", ".#.", ".#.", ".#."],
    "question": [".#.", "#.#", "..#", "...", ".#."],
    "plus": [".#.", ".#.", "###", ".#.", ".#."],
    "minus": ["...", "...", "###", "...", "..."],
    "equals": ["...", "###", "...", "###", "..."],
    "triangle": [".#.", ".#.", "##.", "###", "###"],
    "hourglass": ["###", ".#.", ".#.", ".#.", "###"],
    "bowtie": ["##.", ".#.", ".#.", ".#.", "##."],
    "chevron": [".#.", "#.#", "#.#", "...", "..."],
    "bracket": ["##.", "#..", "#..", "#..", "##."],
    "pillars": ["#.#", "#.#", "#.#", "#.#", "#.#"],
    "arch": [".#.", "#.#", "#.#", "#.#", ".#."],
    "tent": [".#.", "#.#", "###", "#.#", "#.#"],
    "mountain": ["#..", "##.", ".#.", ".##", "###"],
    "wave": ["#..", ".#.", "..#", ".#.", "#.."],
    "spiral": [".#.", "#.#", ".##", "...", ".#."],
    "bitcoin": [".#.", "###", ".#.", "###", ".#."],
}


def render_pattern(name, color, bg=0):
    """Render a named pattern to a list of 15 segment colors."""
    rows = PATTERNS.get(name.lower())
    if rows is None:
        raise ValueError(f"Unknown pixel pattern: {name}")
    colors = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            colors.append(color if rows[r][c] != "." else bg)
    return colors


def render_bits(bits, color, bg=0):
    """Render a bit string (e.g. '101010...') to segment colors."""
    bits = bits.replace(" ", "").replace(",", "")
    colors = []
    for i in range(NUM_SEGMENTS):
        if i < len(bits) and bits[i] not in ("0", ".", "_"):
            colors.append(color)
        else:
            colors.append(bg)
    return colors


def is_bit_string(text):
    """Check if a string looks like a raw bit pattern."""
    cleaned = text.replace(" ", "").replace(",", "")
    if not cleaned:
        return False
    return all(c in "01.#_" for c in cleaned) and any(c in "1#" for c in cleaned)


def list_patterns():
    """Return sorted list of pattern names."""
    return sorted(PATTERNS.keys())
