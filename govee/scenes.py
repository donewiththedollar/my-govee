"""Preset scene combos — sequences of text + animation, ~15-20s total."""

from .colors import parse_color
from . import animations

SCENES = {
    "bitcoin": {
        "steps": [
            {"type": "text", "text": "BTC", "mode": "morse", "color": "bitcoin_orange", "duration": 6},
            {"type": "animate", "name": "bitcoin_orange_pulse", "duration": 5},
            {"type": "animate", "name": "bitcoin_rain", "duration": 6},
        ],
        "brightness": 90,
        "description": "BTC morse, orange pulse, bitcoin rain",
    },
    "whale": {
        "steps": [
            {"type": "animate", "name": "underwater", "duration": 6},
            {"type": "animate", "name": "whale_swim", "duration": 8},
        ],
        "brightness": 80,
        "description": "Underwater then whale swim",
    },
    "goldfish": {
        "steps": [
            {"type": "animate", "name": "lava_lamp", "duration": 5},
            {"type": "animate", "name": "goldfish", "duration": 8},
        ],
        "brightness": 80,
        "description": "Warm glow then goldfish",
    },
    "party": {
        "steps": [
            {"type": "animate", "name": "disco", "duration": 5},
            {"type": "animate", "name": "rainbow_chase", "duration": 5},
            {"type": "animate", "name": "strobe", "duration": 4},
        ],
        "brightness": 100,
        "description": "Disco, rainbow, strobe",
    },
    "cyberpunk": {
        "steps": [
            {"type": "animate", "name": "neon_sunset", "duration": 7},
            {"type": "animate", "name": "cyberpunk", "duration": 8},
        ],
        "brightness": 90,
        "description": "Neon sunset then cyberpunk",
    },
    "galaxy": {
        "steps": [
            {"type": "animate", "name": "galaxy", "duration": 8},
            {"type": "animate", "name": "color_cycle", "duration": 7},
        ],
        "brightness": 80,
        "description": "Galaxy twinkle then color cycle",
    },
    "fire": {
        "steps": [
            {"type": "animate", "name": "flame_core", "duration": 7},
            {"type": "animate", "name": "fire_flicker", "duration": 8},
        ],
        "brightness": 90,
        "description": "Flame core then fire flicker",
    },
    "matrix": {
        "steps": [
            {"type": "animate", "name": "matrix_rain", "duration": 15},
        ],
        "brightness": 80,
        "description": "Matrix rain in green",
    },
    "aurora": {
        "steps": [
            {"type": "animate", "name": "aurora_chase", "duration": 15},
        ],
        "brightness": 80,
        "description": "Aurora chase",
    },
    "ocean": {
        "steps": [
            {"type": "animate", "name": "ocean_wave", "duration": 7},
            {"type": "animate", "name": "underwater", "duration": 8},
        ],
        "brightness": 70,
        "description": "Ocean wave then underwater",
    },
    "sunset": {
        "steps": [
            {"type": "animate", "name": "neon_sunset", "duration": 8},
            {"type": "animate", "name": "sunrise", "duration": 7},
        ],
        "brightness": 80,
        "description": "Neon sunset then sunrise",
    },
}


def get_scene(name):
    name = name.lower()
    if name not in SCENES:
        raise ValueError(f"Unknown scene: {name}. Available: {', '.join(sorted(SCENES))}")
    return SCENES[name]


def list_scenes():
    return sorted(SCENES.keys())
