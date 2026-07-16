"""Pixel patterns — static and animated for the 15-segment display."""

from .font import WIDTH, HEIGHT, NUM_SEGMENTS

PATTERNS = {
    "heart": [".#.", "###", "###", ".#.", ".#."],
    "smiley": [".#.", "#.#", ".#.", "#.#", ".#."],
    "arrow_up": [".#.", "###", ".#.", ".#.", ".#."],
    "arrow_down": [".#.", ".#.", ".#.", "###", ".#."],
    "diamond": [".#.", "###", "###", "###", ".#."],
    "cross": [".#.", ".#.", "###", ".#.", ".#."],
    "checker": ["#.#", ".#.", "#.#", ".#.", "#.#"],
    "border": ["###", "#.#", "#.#", "#.#", "###"],
    "x": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "invader": ["#.#", ".#.", "###", "#.#", "#.#"],
    "ghost": [".#.", "#.#", "#.#", "###", "#.#"],
    "star": [".#.", "#.#", ".#.", "#.#", ".#."],
    "tree": [".#.", "###", "###", ".#.", ".#."],
    "house": [".#.", "###", "#.#", "#.#", "###"],
    "full": ["###", "###", "###", "###", "###"],
    "empty": ["...", "...", "...", "...", "..."],
    "bitcoin": [".#.", "###", ".#.", "###", ".#."],
    "circle": [".#.", "#.#", "#.#", "#.#", ".#."],
    "triangle": [".#.", ".#.", "##.", "###", "###"],
    "hourglass": ["###", ".#.", ".#.", ".#.", "###"],
    "wave": ["#..", ".#.", "..#", ".#.", "#.."],
    "spiral": [".#.", "#.#", ".##", "...", ".#."],
    "chevron": [".#.", "#.#", "#.#", "...", "..."],
    "pillars": ["#.#", "#.#", "#.#", "#.#", "#.#"],
    "tent": [".#.", "#.#", "###", "#.#", "#.#"],
    "mountain": ["#..", "##.", ".#.", ".##", "###"],
    "stairs": ["#..", "##.", "##.", "###", "###"],
    "zigzag": ["#..", "##.", ".##", ".##", "..#"],
    "bowtie": ["##.", ".#.", ".#.", ".#.", "##."],
    "bracket": ["##.", "#..", "#..", "#..", "##."],
    "corners": ["#.#", "...", "...", "...", "#.#"],
    "top": ["###", "#.#", "#.#", "#.#", "#.#"],
    "bottom": ["#.#", "#.#", "#.#", "#.#", "###"],
    "hbar": ["...", "...", "###", "...", "..."],
    "vbar": [".#.", ".#.", ".#.", ".#.", ".#."],
    "dot": ["...", ".#.", ".#.", ".#.", "..."],
    "plus": [".#.", ".#.", "###", ".#.", ".#."],
    "minus": ["...", "...", "###", "...", "..."],
    "t": ["###", ".#.", ".#.", ".#.", ".#."],
    "note": [".#.", ".#.", "###", "###", ".#."],
    "cup": [".#.", "###", "#.#", "#.#", "###"],
    "arch": [".#.", "#.#", "#.#", "#.#", ".#."],
    "exclaim": [".#.", ".#.", ".#.", ".#.", ".#."],
    "question": [".#.", "#.#", "..#", "...", ".#."],
    "equals": ["...", "###", "...", "###", "..."],
}

ANIMATED_PATTERNS = {
    "loading": [
        ["#..", "...", "...", "...", "..."],
        [".#.", "...", "...", "...", "..."],
        ["..#", "...", "...", "...", "..."],
        ["...", "..#", "...", "...", "..."],
        ["...", ".#.", "...", "...", "..."],
        ["...", "#..", "...", "...", "..."],
        ["...", "...", "#..", "...", "..."],
        ["...", "...", ".#.", "...", "..."],
        ["...", "...", "..#", "...", "..."],
        ["...", "...", "...", "..#", "..."],
        ["...", "...", "...", ".#.", "..."],
        ["...", "...", "...", "#..", "..."],
    ],
    "bounce_dot": [
        [".#.", "...", "...", "...", "..."],
        ["...", ".#.", "...", "...", "..."],
        ["...", "...", ".#.", "...", "..."],
        ["...", "...", "...", ".#.", "..."],
        ["...", "...", "...", "...", ".#."],
        ["...", "...", "...", ".#.", "..."],
        ["...", "...", ".#.", "...", "..."],
        ["...", ".#.", "...", "...", "..."],
    ],
    "expand": [
        ["...", "...", ".#.", "...", "..."],
        ["...", ".#.", ".#.", ".#.", "..."],
        [".#.", ".#.", ".#.", ".#.", ".#."],
        ["###", "###", "###", "###", "###"],
        [".#.", ".#.", ".#.", ".#.", ".#."],
        ["...", ".#.", ".#.", ".#.", "..."],
        ["...", "...", ".#.", "...", "..."],
    ],
    "wipe": [
        ["#..", "#..", "#..", "#..", "#.."],
        ["##.", "##.", "##.", "##.", "##."],
        ["###", "###", "###", "###", "###"],
        [".##", ".##", ".##", ".##", ".##"],
        ["..#", "..#", "..#", "..#", "..#"],
        ["...", "...", "...", "...", "..."],
    ],
}


def render_pattern(name, color, bg=0):
    rows = PATTERNS.get(name.lower())
    if rows is None:
        raise ValueError(f"Unknown pattern: {name}")
    colors = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            colors.append(color if rows[r][c] != "." else bg)
    return colors


def render_bits(bits, color, bg=0):
    bits = bits.replace(" ", "").replace(",", "")
    colors = []
    for i in range(NUM_SEGMENTS):
        if i < len(bits) and bits[i] not in ("0", ".", "_"):
            colors.append(color)
        else:
            colors.append(bg)
    return colors


def render_custom(values):
    colors = []
    for i in range(NUM_SEGMENTS):
        if i < len(values):
            colors.append(int(values[i]))
        else:
            colors.append(0)
    return colors


def get_animated_pattern(name, color, bg=0):
    frames = ANIMATED_PATTERNS.get(name.lower())
    if frames is None:
        raise ValueError(f"Unknown animated pattern: {name}")
    result = []
    for rows in frames:
        colors = []
        for r in range(HEIGHT):
            for c in range(WIDTH):
                colors.append(color if rows[r][c] != "." else bg)
        result.append(colors)
    return result


def is_bit_string(text):
    cleaned = text.replace(" ", "").replace(",", "")
    if not cleaned:
        return False
    return all(c in "01.#_" for c in cleaned) and any(c in "1#" for c in cleaned)


def list_patterns():
    return sorted(PATTERNS.keys())


def list_animated_patterns():
    return sorted(ANIMATED_PATTERNS.keys())
