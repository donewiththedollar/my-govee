"""Scene preset library combining animations, colors, and brightness."""

from .colors import parse_color
from . import animations

SCENES = {
    "bitcoin": {
        "animation": "pulse",
        "color": "bitcoin",
        "brightness": 100,
        "frame_interval": 0.6,
        "description": "Bitcoin orange pulse",
    },
    "matrix": {
        "animation": "matrix_rain",
        "color": "matrix",
        "brightness": 80,
        "frame_interval": 0.5,
        "description": "Matrix digital rain",
    },
    "fire": {
        "animation": "fire_flicker",
        "color": "fire",
        "brightness": 90,
        "frame_interval": 0.5,
        "description": "Fire flicker",
    },
    "ocean": {
        "animation": "ocean_wave",
        "color": "ocean",
        "brightness": 70,
        "frame_interval": 0.6,
        "description": "Ocean wave",
    },
    "aurora": {
        "animation": "aurora_chase",
        "color": "aurora",
        "brightness": 80,
        "frame_interval": 0.6,
        "description": "Aurora chase",
    },
    "rainbow": {
        "animation": "rainbow_chase",
        "color": None,
        "brightness": 90,
        "frame_interval": 0.6,
        "description": "Rainbow chase",
    },
    "lightning": {
        "animation": "lightning_flash",
        "color": "white",
        "brightness": 100,
        "frame_interval": 0.4,
        "description": "Lightning flash",
    },
    "heartbeat": {
        "animation": "heartbeat",
        "color": "crimson",
        "brightness": 100,
        "frame_interval": 0.4,
        "description": "Heartbeat",
    },
    "police": {
        "animation": "police",
        "color": None,
        "brightness": 100,
        "frame_interval": 0.3,
        "description": "Police lights",
    },
    "candle": {
        "animation": "candle",
        "color": "orange",
        "brightness": 70,
        "frame_interval": 0.4,
        "description": "Candle flicker",
    },
    "strobe": {
        "animation": "strobe",
        "color": "white",
        "brightness": 100,
        "frame_interval": 0.3,
        "description": "Strobe light",
    },
    "sunrise": {
        "animation": "sunrise",
        "color": "orange",
        "brightness": 80,
        "frame_interval": 0.6,
        "description": "Sunrise / sunset",
    },
    "bounce": {
        "animation": "color_bounce",
        "color": "cyan",
        "brightness": 90,
        "frame_interval": 0.4,
        "description": "Bouncing light",
    },
    "twinkle": {
        "animation": "twinkle",
        "color": "white",
        "brightness": 80,
        "frame_interval": 0.4,
        "description": "Twinkling stars",
    },
    "breathe": {
        "animation": "breathe",
        "color": "purple",
        "brightness": 80,
        "frame_interval": 0.6,
        "description": "Breathing purple",
    },
}


def get_scene(name):
    """Look up a scene configuration by name."""
    name = name.lower()
    if name not in SCENES:
        raise ValueError(f"Unknown scene: {name}. Available: {', '.join(sorted(SCENES))}")
    return SCENES[name]


def build_scene_frames(scene):
    """Build an infinite frame generator from a scene config."""
    anim_fn = animations.get_animation(scene["animation"])
    color = scene.get("color")
    color_int = parse_color(color) if color else None
    return anim_fn(color=color_int)


def list_scenes():
    """Return sorted scene names."""
    return sorted(SCENES.keys())
