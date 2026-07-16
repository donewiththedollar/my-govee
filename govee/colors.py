"""Color library for the Govee display engine."""

NAMED_COLORS = {
    "red": 0xFF0000, "green": 0x00FF00, "blue": 0x0000FF,
    "purple": 0x800080, "orange": 0xFF8000, "yellow": 0xFFFF00,
    "white": 0xFFFFFF, "cyan": 0x00FFFF, "magenta": 0xFF00FF,
    "pink": 0xFF69B4, "gold": 0xFFD700, "teal": 0x008080,
    "lime": 0x32CD32, "coral": 0xFF7F50, "navy": 0x000080,
    "maroon": 0x800000, "turquoise": 0x40E0D0, "salmon": 0xFA8072,
    "crimson": 0xDC143C, "violet": 0xEE82EE, "indigo": 0x4B0082,
    "bitcoin_orange": 0xF7931A, "aqua": 0x00FFFF, "sky_blue": 0x87CEEB,
    "mint": 0x98FF98, "lavender": 0xB57EDC, "black": 0x000000,
    "gray": 0x808080, "grey": 0x808080, "silver": 0xC0C0C0,
    "ice": 0x00BFFF, "fire": 0xFF4500, "ocean": 0x0077BE,
    "aurora": 0x00FF7F, "matrix": 0x00FF41, "neon": 0x39FF14,
    "amber": 0xFFBF00, "emerald": 0x50C878, "ruby": 0xE0115F,
    "sapphire": 0x0F52BA, "rose": 0xFF007F, "azure": 0xF0FFFF,
    "chartreuse": 0x7FFF00, "springgreen": 0x00FF7F,
    "dodgerblue": 0x1E90FF, "hotpink": 0xFF69B4,
    "lawngreen": 0x7CFC00, "gold": 0xFFD700,
    "deepskyblue": 0x00BFFF, "forestgreen": 0x228B22,
    "darkorange": 0xFF8C00, "darkviolet": 0x9400D3,
    "orangered": 0xFF4500, "royalblue": 0x4169E1,
    "seagreen": 0x2E8B57, "slateblue": 0x6A5ACD,
    "steelblue": 0x4682B4, "darkred": 0x8B0000,
    "darkgreen": 0x006400, "darkblue": 0x00008B,
    "lightblue": 0xADD8E6, "lightgreen": 0x90EE90,
    "lightcoral": 0xF08080, "lightpink": 0xFFB6C1,
    "mediumseagreen": 0x3CB371, "mediumorchid": 0xBA55D3,
    "mediumslateblue": 0x7B68EE, "midnightblue": 0x191970,
    "sandybrown": 0xF4A460, "saddlebrown": 0x8B4513,
    "sienna": 0xA0522D, "tomato": 0xFF6347,
    "wheat": 0xF5DEB3, "khaki": 0xF0E68C,
    "plum": 0xDDA0DD, "orchid": 0xDA70D6,
    "thistle": 0xD8BFD8, "peru": 0xCD853F,
    "chocolate": 0xD2691E, "tan": 0xD2B48C,
    "linen": 0xFAF0E6, "ivory": 0xFFFFF0,
    "snow": 0xFFFAFA, "whitesmoke": 0xF5F5F5,
    "aliceblue": 0xF0F8FF, "honeydew": 0xF0FFF0,
    "mintcream": 0xF5FFFA, "azure": 0xF0FFFF,
    "ghostwhite": 0xF8F8FF, "seashell": 0xFFF5EE,
    "oldlace": 0xFDF5E6, "floralwhite": 0xFFFAF0,
    "papayawhip": 0xFFEFD5, "blanchedalmond": 0xFFEBCD,
    "bisque": 0xFFE4C4, "moccasin": 0xFFE4B5,
    "navajowhite": 0xFFDEAD, "peachpuff": 0xFFDAB9,
    "mistyrose": 0xFFE4E1, "cornsilk": 0xFFF8DC,
    "lemonchiffon": 0xFFFACD, "lightyellow": 0xFFFFE0,
    "lightcyan": 0xE0FFFF, "paleturquoise": 0xAFEEEE,
    "powderblue": 0xB0E0E6, "lightsteelblue": 0xB0C4DE,
    "lightskyblue": 0x87CEFA, "skyblue": 0x87CEEB,
    "lightseagreen": 0x20B2AA, "darkturquoise": 0x00CED1,
    "cadetblue": 0x5F9EA0, "darkcyan": 0x008B8B,
    "darkslategray": 0x2F4F4F, "darkslategrey": 0x2F4F4F,
    "mediumturquoise": 0x48D1CC, "mediumaquamarine": 0x66CDAA,
    "aquamarine": 0x7FFFD4, "palegreen": 0x98FB98,
    "darkseagreen": 0x8FBC8F, "darkolivegreen": 0x556B2F,
    "olive": 0x808000, "olivedrab": 0x6B8E23,
    "yellowgreen": 0x9ACD32, "greenyellow": 0xADFF2F,
    "chartreuse": 0x7FFF00, "lawngreen": 0x7CFC00,
    "darkkhaki": 0xBDB76B, "palegoldenrod": 0xEEE8AA,
    "goldenrod": 0xDAA520, "darkgoldenrod": 0xB8860B,
    "rosybrown": 0xBC8F8F, "indianred": 0xCD5C5C,
    "lightcoral": 0xF08080, "darksalmon": 0xE9967A,
    "lightsalmon": 0xFFA07A, "burlywood": 0xDEB887,
    "navajowhite": 0xFFDEAD, "wheat": 0xF5DEB3,
    "sandybrown": 0xF4A460, "chocolate": 0xD2691E,
    "peru": 0xCD853F, "firebrick": 0xB22222,
    "brown": 0xA52A2A, "darkred": 0x8B0000,
    "maroon": 0x800000, "mediumvioletred": 0xC71585,
    "palevioletred": 0xDB7093, "deeppink": 0xFF1493,
    "hotpink": 0xFF69B4, "lightpink": 0xFFB6C1,
    "pink": 0xFFC0CB, "orchid": 0xDA70D6,
    "plum": 0xDDA0DD, "violet": 0xEE82EE,
    "mediumorchid": 0xBA55D3, "darkorchid": 0x9932CC,
    "darkviolet": 0x9400D3, "blueviolet": 0x8A2BE2,
    "purple": 0x800080, "mediumpurple": 0x9370DB,
    "thistle": 0xD8BFD8, "slateblue": 0x6A5ACD,
    "mediumslateblue": 0x7B68EE, "darkslateblue": 0x483D8B,
    "rebeccapurple": 0x663399, "indigo": 0x4B0082,
    "darkblue": 0x00008B, "mediumblue": 0x0000CD,
    "royalblue": 0x4169E1, "dodgerblue": 0x1E90FF,
    "cornflowerblue": 0x6495ED, "lightskyblue": 0x87CEFA,
    "skyblue": 0x87CEEB, "deepskyblue": 0x00BFFF,
    "steelblue": 0x4682B4, "lightsteelblue": 0xB0C4DE,
    "powderblue": 0xB0E0E6, "paleturquoise": 0xAFEEEE,
    "darkslategray": 0x2F4F4F, "darkslategrey": 0x2F4F4F,
    "dimgray": 0x696969, "dimgrey": 0x696969,
    "slategray": 0x708090, "slategrey": 0x708090,
    "lightslategray": 0x778899, "lightslategrey": 0x778899,
    "gray": 0x808080, "grey": 0x808080,
    "darkgray": 0xA9A9A9, "darkgrey": 0xA9A9A9,
    "lightgray": 0xD3D3D3, "lightgrey": 0xD3D3D3,
    "gainsboro": 0xDCDCDC, "whitesmoke": 0xF5F5F5,
    "seashell": 0xFFF5EE, "beige": 0xF5F5DC,
    "oldlace": 0xFDF5E6, "floralwhite": 0xFFFAF0,
    "ivory": 0xFFFFF0, "antiquewhite": 0xFAEBD7,
    "linen": 0xFAF0E6, "lavenderblush": 0xFFF0F5,
    "mistyrose": 0xFFE4E1, "snow": 0xFFFAFA,
    "white": 0xFFFFFF, "black": 0x000000,
}


def rgb_to_int(r, g, b):
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return (r << 16) | (g << 8) | b


def int_to_rgb(value):
    value = int(value) & 0xFFFFFF
    return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)


def hex_to_int(text):
    text = text.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(c * 2 for c in text)
    return int(text, 16)


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = int_to_rgb(c1)
    r2, g2, b2 = int_to_rgb(c2)
    return rgb_to_int(r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)


def hsv_to_rgb(h, s=1.0, v=1.0):
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
    r, g, b = int_to_rgb(color)
    return rgb_to_int(r * factor, g * factor, b * factor)


def color_distance(c1, c2):
    r1, g1, b1 = int_to_rgb(c1)
    r2, g2, b2 = int_to_rgb(c2)
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def quantize_frame(colors, max_colors=6):
    from collections import Counter
    color_list = [int(c) for c in colors]
    unique = set(color_list)
    if len(unique) <= max_colors:
        return color_list
    counter = Counter(color_list)
    palette = [c for c, _ in counter.most_common(max_colors)]
    palette_set = set(palette)
    result = []
    for c in color_list:
        if c in palette_set:
            result.append(c)
        else:
            result.append(min(palette, key=lambda p: color_distance(c, p)))
    return result


def parse_color(value, default=0xFFFFFF):
    if value is None:
        return default
    if isinstance(value, int):
        return value
    text = str(value).strip().lower()
    if not text:
        return default
    if text in NAMED_COLORS:
        return NAMED_COLORS[text]
    if "," in text:
        parts = text.split(",")
        if len(parts) == 3:
            return rgb_to_int(int(parts[0]), int(parts[1]), int(parts[2]))
    try:
        return hex_to_int(text)
    except (ValueError, TypeError):
        raise ValueError(f"Unknown color: {value!r}")
