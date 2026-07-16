"""Color utilities for the Govee display controller."""

NAMED_COLORS = {
    "black": 0x000000,
    "white": 0xFFFFFF,
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "cyan": 0x00FFFF,
    "magenta": 0xFF00FF,
    "orange": 0xFF8000,
    "purple": 0x800080,
    "pink": 0xFF69B4,
    "lime": 0x32CD32,
    "teal": 0x008080,
    "navy": 0x000080,
    "maroon": 0x800000,
    "olive": 0x808000,
    "silver": 0xC0C0C0,
    "gray": 0x808080,
    "grey": 0x808080,
    "gold": 0xFFD700,
    "bitcoin": 0xF7931A,
    "matrix": 0x00FF41,
    "fire": 0xFF4500,
    "ocean": 0x0077BE,
    "aurora": 0x00FF7F,
    "ice": 0x00BFFF,
    "crimson": 0xDC143C,
    "indigo": 0x4B0082,
    "violet": 0xEE82EE,
    "amber": 0xFFBF00,
    "coral": 0xFF7F50,
    "mint": 0x98FF98,
    "sky": 0x87CEEB,
    "rose": 0xFF007F,
    "emerald": 0x50C878,
    "ruby": 0xE0115F,
    "sapphire": 0x0F52BA,
    "neon": 0x39FF14,
    "lavender": 0xB57EDC,
    "salmon": 0xFA8072,
    "khaki": 0xF0E68C,
    "plum": 0xDDA0DD,
    "orchid": 0xDA70D6,
    "tan": 0xD2B48C,
    "wheat": 0xF5DEB3,
    "ivory": 0xFFFFF0,
    "snow": 0xFFFAFA,
    "azure": 0xF0FFFF,
    "beige": 0xF5F5DC,
    "chartreuse": 0x7FFF00,
    "turquoise": 0x40E0D0,
    "springgreen": 0x00FF7F,
    "dodgerblue": 0x1E90FF,
    "hotpink": 0xFF69B4,
    "lawngreen": 0x7CFC00,
    "mediumseagreen": 0x3CB371,
    "mediumorchid": 0xBA55D3,
    "mediumslateblue": 0x7B68EE,
    "midnightblue": 0x191970,
    "orangered": 0xFF4500,
    "royalblue": 0x4169E1,
    "seagreen": 0x2E8B57,
    "slateblue": 0x6A5ACD,
    "steelblue": 0x4682B4,
    "darkorange": 0xFF8C00,
    "darkviolet": 0x9400D3,
    "deepskyblue": 0x00BFFF,
    "forestgreen": 0x228B22,
    "goldenrod": 0xDAA520,
    "indianred": 0xCD5C5C,
    "lightcoral": 0xF08080,
    "mediumvioletred": 0xC71585,
    "olivedrab": 0x6B8E23,
    "orange": 0xFFA500,
    "orangered": 0xFF4500,
    "sandybrown": 0xF4A460,
    "darkgreen": 0x006400,
    "darkcyan": 0x008B8B,
    "darkblue": 0x00008B,
    "darkred": 0x8B0000,
    "darkmagenta": 0x8B008B,
    "darkgray": 0xA9A9A9,
    "darkgrey": 0xA9A9A9,
    "lightgray": 0xD3D3D3,
    "lightgrey": 0xD3D3D3,
    "lightpink": 0xFFB6C1,
    "lightsalmon": 0xFFA07A,
    "lightgreen": 0x90EE90,
    "lightblue": 0xADD8E6,
    "lightyellow": 0xFFFFE0,
    "lightcyan": 0xE0FFFF,
    "lightseagreen": 0x20B2AA,
    "lightskyblue": 0x87CEFA,
    "lightslategray": 0x778899,
    "lightslategrey": 0x778899,
    "limegreen": 0x32CD32,
    "linen": 0xFAF0E6,
    "mediumaquamarine": 0x66CDAA,
    "mediumblue": 0x0000CD,
    "mediumturquoise": 0x48D1CC,
    "mistyrose": 0xFFE4E1,
    "moccasin": 0xFFE4B5,
    "oldlace": 0xFDF5E6,
    "olive": 0x808000,
    "palegoldenrod": 0xEEE8AA,
    "palegreen": 0x98FB98,
    "paleturquoise": 0xAFEEEE,
    "palevioletred": 0xDB7093,
    "papayawhip": 0xFFEFD5,
    "peachpuff": 0xFFDAB9,
    "peru": 0xCD853F,
    "powderblue": 0xB0E0E6,
    "rebeccapurple": 0x663399,
    "rosybrown": 0xBC8F8F,
    "saddlebrown": 0x8B4513,
    "sienna": 0xA0522D,
    "slategray": 0x708090,
    "slategrey": 0x708090,
    "thistle": 0xD8BFD8,
    "tomato": 0xFF6347,
    "whitesmoke": 0xF5F5F5,
    "yellowgreen": 0x9ACD32,
}


def rgb_to_int(r, g, b):
    """Convert RGB channels (0-255) to a packed integer."""
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return (r << 16) | (g << 8) | b


def int_to_rgb(value):
    """Convert a packed integer color to an (r, g, b) tuple."""
    value = int(value) & 0xFFFFFF
    return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)


def hex_to_int(text):
    """Convert a hex color string (with or without #) to an integer."""
    text = text.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(c * 2 for c in text)
    return int(text, 16)


def lerp_color(c1, c2, t):
    """Linearly interpolate between two integer colors. t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = int_to_rgb(c1)
    r2, g2, b2 = int_to_rgb(c2)
    return rgb_to_int(
        r1 + (r2 - r1) * t,
        g1 + (g2 - g1) * t,
        b1 + (b2 - b1) * t,
    )


def hsv_to_rgb(h, s=1.0, v=1.0):
    """Convert HSV to a packed integer color. h in [0, 360), s/v in [0, 1]."""
    h = h % 360.0
    s = max(0.0, min(1.0, s))
    v = max(0.0, min(1.0, v))
    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    if h < 60:
        rp, gp, bp = c, x, 0
    elif h < 120:
        rp, gp, bp = x, c, 0
    elif h < 180:
        rp, gp, bp = 0, c, x
    elif h < 240:
        rp, gp, bp = 0, x, c
    elif h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x
    return rgb_to_int((rp + m) * 255, (gp + m) * 255, (bp + m) * 255)


def scale_color(color, factor):
    """Scale a color's brightness by a factor (0.0 - 1.0+)."""
    r, g, b = int_to_rgb(color)
    return rgb_to_int(r * factor, g * factor, b * factor)


def parse_color(value, default=0xFFFFFF):
    """Parse a color from a name, hex string, or integer."""
    if value is None:
        return default
    if isinstance(value, int):
        return value
    text = str(value).strip().lower()
    if not text:
        return default
    if text in NAMED_COLORS:
        return NAMED_COLORS[text]
    try:
        return hex_to_int(text)
    except (ValueError, TypeError):
        raise ValueError(f"Unknown color: {value!r}")
