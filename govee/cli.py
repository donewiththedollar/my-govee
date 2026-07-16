"""Command-line interface for the Govee display controller."""

import argparse
import json
import sys
import time

from .client import GoveeClient, GoveeConfigError
from .colors import parse_color, NAMED_COLORS
from .display import GoveeDisplay
from . import text as text_mod
from . import pixel as pixel_mod
from . import animations as anim_mod
from . import scenes as scenes_mod


def _make_client(args):
    return GoveeClient(
        api_key=getattr(args, "api_key", None),
        device=getattr(args, "device", None),
        sku=getattr(args, "sku", None),
        dry_run=getattr(args, "dry_run", False),
    )


def _make_display(args):
    max_colors = getattr(args, "max_colors", 0) or 0
    return GoveeDisplay(_make_client(args), max_colors=max_colors)


def cmd_text(args):
    display = _make_display(args)
    if args.color.lower() == "auto":
        color = None
    else:
        color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    text = args.text.upper()
    if args.mode == "scroll":
        frames = text_mod.scroll_frames(text, color=color, bg=0)
    else:
        frames = text_mod.flash_frames(
            text, color=color, bg=0, blank=not args.no_blank, solid=args.solid
        )
    interval = args.interval if args.interval is not None else 1.0
    count = display.run_frames(
        frames, duration=args.duration, frame_interval=interval,
        on_stop_clear=not args.keep,
    )
    print(f"Displayed {count} frames.")


def cmd_animate(args):
    display = _make_display(args)
    anim_fn = anim_mod.get_animation(args.name)
    color = parse_color(args.color) if args.color else None
    frames = anim_fn(color=color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    interval = args.interval if args.interval is not None else 0.6
    count = display.run_frames(
        frames, duration=args.duration, frame_interval=interval,
        on_stop_clear=not args.keep,
    )
    print(f"Rendered {count} frames.")


def cmd_pixel(args):
    display = _make_display(args)
    color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    if args.pattern.lower() in pixel_mod.PATTERNS:
        frame = pixel_mod.render_pattern(args.pattern, color)
    elif pixel_mod.is_bit_string(args.pattern):
        frame = pixel_mod.render_bits(args.pattern, color)
    else:
        print(f"Unknown pattern: {args.pattern}. "
              f"Use 'list patterns' to see options.", file=sys.stderr)
        sys.exit(1)
    display.render(frame)
    print(f"Rendered pixel pattern: {args.pattern}")


def cmd_scene(args):
    display = _make_display(args)
    scene = scenes_mod.get_scene(args.name)
    if args.brightness is not None:
        display.brightness(args.brightness)
    else:
        display.brightness(scene.get("brightness", 80))
    frames = scenes_mod.build_scene_frames(scene)
    interval = args.interval if args.interval is not None else scene.get("frame_interval", 0.6)
    count = display.run_frames(
        frames, duration=args.duration, frame_interval=interval,
        on_stop_clear=not args.keep,
    )
    print(f"Scene '{args.name}' ({scene['description']}) ran {count} frames.")


def cmd_state(args):
    client = _make_client(args)
    state = client.get_state()
    print(json.dumps(state, indent=2))


def cmd_clear(args):
    display = _make_display(args)
    display.clear()
    print("Display cleared.")


def cmd_power(args):
    client = _make_client(args)
    client.set_power(args.on)
    print(f"Power {'on' if args.on else 'off'}.")


def cmd_brightness(args):
    client = _make_client(args)
    client.set_brightness(args.value)
    print(f"Brightness set to {args.value}.")


def cmd_color(args):
    display = _make_display(args)
    color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    display.set_color(color)
    print(f"Color set to {args.color} (0x{color:06X}).")


def cmd_test(args):
    """Light each segment 0-14 one at a time for physical calibration."""
    display = _make_display(args)
    color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    from .font import NUM_SEGMENTS
    try:
        for i in range(NUM_SEGMENTS):
            frame = [0] * NUM_SEGMENTS
            frame[i] = color
            display.render(frame)
            print(f"\rSegment {i:2d}/{NUM_SEGMENTS - 1}", end="", flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        display.clear()
        print("\nSegment test complete.")


def cmd_segments(args):
    """Print the segment index to grid position mapping."""
    from .font import WIDTH, HEIGHT, NUM_SEGMENTS
    print(f"Grid: {WIDTH} wide x {HEIGHT} tall = {NUM_SEGMENTS} segments")
    print(f"Mapping (row-major, segment = row * {WIDTH} + col):\n")
    for r in range(HEIGHT):
        cells = []
        for c in range(WIDTH):
            idx = r * WIDTH + c
            cells.append(f"seg{idx:2d}")
        print("  " + "  ".join(cells))


def cmd_list(args):
    if args.what == "animations":
        print("Animations: " + ", ".join(anim_mod.list_animations()))
    elif args.what == "scenes":
        print("Scenes: " + ", ".join(scenes_mod.list_scenes()))
    elif args.what == "patterns":
        print("Patterns: " + ", ".join(pixel_mod.list_patterns()))
    elif args.what == "colors":
        print("Colors: " + ", ".join(sorted(NAMED_COLORS)))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="govee_display",
        description="Govee H6022 Quantum Desk Lamp display controller.",
    )
    parser.add_argument("--api-key", default=None,
                        help="Govee API key (env: GOVEE_API_KEY)")
    parser.add_argument("--device", default=None,
                        help="Device BLE address (env: GOVEE_DEVICE)")
    parser.add_argument("--sku", default=None,
                        help="Device SKU/model (env: GOVEE_SKU, default: H6022)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview frames locally without API calls")
    sub = parser.add_subparsers(dest="command", required=True)

    p_text = sub.add_parser("text", help="Display scrolling/flashing text")
    p_text.add_argument("text", help="Text to display")
    p_text.add_argument("--color", default="auto",
                        help="Text color or 'auto' for per-letter unique colors")
    p_text.add_argument("--mode", choices=["flash", "scroll"], default="flash",
                        help="flash = one letter at a time, scroll = marquee")
    p_text.add_argument("--solid", action="store_true",
                        help="Light ALL segments per letter (max visibility on 1D strip)")
    p_text.add_argument("--no-blank", action="store_true",
                         help="Skip blank frame between letters")
    p_text.add_argument("--duration", type=float, default=None,
                        help="Seconds to run (default: forever)")
    p_text.add_argument("--interval", type=float, default=None,
                        help="Seconds per frame (default: 1.0)")
    p_text.add_argument("--brightness", type=int, default=None,
                        help="Brightness 0-100")
    p_text.add_argument("--max-colors", type=int, default=0,
                        help="Quantize to N colors max per frame (0 = no limit)")
    p_text.add_argument("--keep", action="store_true",
                        help="Do not clear display on exit")
    p_text.set_defaults(func=cmd_text)

    p_anim = sub.add_parser("animate", help="Run an animation")
    p_anim.add_argument("name", help="Animation name")
    p_anim.add_argument("--color", default=None, help="Override animation color")
    p_anim.add_argument("--duration", type=float, default=None,
                        help="Seconds to run (default: forever)")
    p_anim.add_argument("--interval", type=float, default=None,
                        help="Seconds per frame (default: 0.6)")
    p_anim.add_argument("--brightness", type=int, default=None)
    p_anim.add_argument("--max-colors", type=int, default=6,
                        help="Quantize to N colors per frame (default: 6, 0 = no limit)")
    p_anim.add_argument("--keep", action="store_true")
    p_anim.set_defaults(func=cmd_animate)

    p_pixel = sub.add_parser("pixel", help="Render a pixel art pattern")
    p_pixel.add_argument("pattern", help="Pattern name or bit string (e.g. 101010...)")
    p_pixel.add_argument("--color", default="white")
    p_pixel.add_argument("--brightness", type=int, default=None)
    p_pixel.set_defaults(func=cmd_pixel)

    p_scene = sub.add_parser("scene", help="Run a scene preset")
    p_scene.add_argument("name", help="Scene name")
    p_scene.add_argument("--duration", type=float, default=None)
    p_scene.add_argument("--interval", type=float, default=None)
    p_scene.add_argument("--brightness", type=int, default=None)
    p_scene.add_argument("--max-colors", type=int, default=6,
                        help="Quantize to N colors per frame (default: 6, 0 = no limit)")
    p_scene.add_argument("--keep", action="store_true")
    p_scene.set_defaults(func=cmd_scene)

    p_state = sub.add_parser("state", help="Get device state")
    p_state.set_defaults(func=cmd_state)

    p_clear = sub.add_parser("clear", help="Clear the display")
    p_clear.set_defaults(func=cmd_clear)

    p_power = sub.add_parser("power", help="Turn lamp on or off")
    p_power.add_argument("state", choices=["on", "off"])
    p_power.set_defaults(func=cmd_power, on=None)

    p_bright = sub.add_parser("brightness", help="Set brightness")
    p_bright.add_argument("value", type=int, help="Brightness 0-100")
    p_bright.set_defaults(func=cmd_brightness)

    p_color = sub.add_parser("color", help="Set whole-lamp color")
    p_color.add_argument("color", help="Color name or hex")
    p_color.add_argument("--brightness", type=int, default=None)
    p_color.set_defaults(func=cmd_color)

    p_list = sub.add_parser("list", help="List available items")
    p_list.add_argument("what", choices=["animations", "scenes", "patterns", "colors"])
    p_list.set_defaults(func=cmd_list)

    p_test = sub.add_parser("test", help="Light each segment in sequence (calibration)")
    p_test.add_argument("--color", default="white")
    p_test.add_argument("--interval", type=float, default=0.5,
                        help="Seconds per segment")
    p_test.add_argument("--brightness", type=int, default=None)
    p_test.set_defaults(func=cmd_test)

    p_seg = sub.add_parser("segments", help="Show segment-to-grid mapping")
    p_seg.set_defaults(func=cmd_segments)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "power":
        args.on = args.state == "on"
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except GoveeConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
