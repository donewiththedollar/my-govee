"""Full CLI for the Govee H6022 display engine."""

import argparse
import json
import sys
import time

from .client import GoveeClient, GoveeAPIError
from .colors import parse_color, NAMED_COLORS, rgb_to_int
from .display import GoveeDisplay, DEFAULT_DURATION
from .font import NUM_SEGMENTS
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
        debug=getattr(args, "debug", False),
    )


def _make_display(args):
    mc = getattr(args, "max_colors", 0) or 0
    return GoveeDisplay(_make_client(args), max_colors=mc)


def _resolve_duration(args):
    if getattr(args, "forever", False):
        return None
    return args.duration if args.duration is not None else DEFAULT_DURATION


def cmd_power(args):
    client = _make_client(args)
    client.set_power(args.state == "on")
    print(f"Power {'on' if args.state == 'on' else 'off'}.")


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


def cmd_segments(args):
    display = _make_display(args)
    if args.brightness is not None:
        display.brightness(args.brightness)
    frame = [0] * NUM_SEGMENTS
    for spec in args.specs:
        if ":" not in spec:
            print(f"Invalid segment spec: {spec}", file=sys.stderr)
            sys.exit(1)
        seg_part, color_part = spec.rsplit(":", 1)
        color = parse_color(color_part)
        if "-" in seg_part:
            lo, hi = seg_part.split("-", 1)
            for i in range(int(lo), int(hi) + 1):
                if 0 <= i < NUM_SEGMENTS:
                    frame[i] = color
        else:
            i = int(seg_part)
            if 0 <= i < NUM_SEGMENTS:
                frame[i] = color
    display.render(frame)
    print(f"Set {len([c for c in frame if c])} segments.")


def cmd_text(args):
    display = _make_display(args)
    color = parse_color(args.color) if args.color and args.color.lower() != "auto" else None
    if args.brightness is not None:
        display.brightness(args.brightness)
    text = args.text.upper()
    duration = _resolve_duration(args)
    speed = args.speed if args.speed else 1.0
    mode = args.mode
    if mode == "morse":
        c = color if color is not None else 0xFFFFFF
        gen = text_mod.morse_frames(text, color=c, speed=speed)
        count = display.run_timed_color_frames(gen, duration=duration, on_stop_clear=not args.keep)
    elif mode == "flash":
        gen = text_mod.flash_frames(text, color=color)
        count = display.run_color_frames(gen, duration=duration, frame_interval=1.0 / speed,
                                         on_stop_clear=not args.keep)
    elif mode == "scroll":
        gen = text_mod.scroll_frames(text, color=color)
        count = display.run_frames(gen, duration=duration, frame_interval=0.5 / speed,
                                   on_stop_clear=not args.keep)
    else:
        gen = text_mod.segment_map_frames(text, color=color)
        count = display.run_frames(gen, duration=duration, frame_interval=0.8 / speed,
                                   on_stop_clear=not args.keep)
    print(f"Displayed {count} frames.")


def cmd_animate(args):
    display = _make_display(args)
    anim_fn = anim_mod.get_animation(args.name)
    color = parse_color(args.color) if args.color else None
    frames = anim_fn(color=color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    duration = _resolve_duration(args)
    interval = args.interval if args.interval is not None else 0.6
    count = display.run_frames(frames, duration=duration, frame_interval=interval,
                               on_stop_clear=not args.keep)
    print(f"Rendered {count} frames.")


def cmd_scene(args):
    display = _make_display(args)
    scene = scenes_mod.get_scene(args.name)
    brightness = args.brightness if args.brightness is not None else scene.get("brightness", 80)
    count = display.run_scene(scene, brightness=brightness)
    print(f"Scene '{args.name}' ({scene['description']}) ran {count} frames.")


def cmd_pixel(args):
    display = _make_display(args)
    color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    if args.pattern.lower() in pixel_mod.PATTERNS:
        frame = pixel_mod.render_pattern(args.pattern, color)
        display.render(frame)
        print(f"Rendered pixel pattern: {args.pattern}")
    elif args.pattern.lower() in pixel_mod.ANIMATED_PATTERNS:
        frames = pixel_mod.get_animated_pattern(args.pattern, color)
        duration = _resolve_duration(args)
        count = display.run_frames(frames, duration=duration, frame_interval=0.3,
                                   on_stop_clear=not args.keep)
        print(f"Animated pixel pattern '{args.pattern}': {count} frames.")
    elif pixel_mod.is_bit_string(args.pattern):
        frame = pixel_mod.render_bits(args.pattern, color)
        display.render(frame)
        print(f"Rendered bit pattern.")
    else:
        try:
            data = json.loads(args.pattern)
            if isinstance(data, list):
                if data and isinstance(data[0], list):
                    duration = _resolve_duration(args)
                    count = display.run_frames(data, duration=duration, frame_interval=0.3,
                                               on_stop_clear=not args.keep)
                    print(f"Animated JSON pattern: {count} frames.")
                else:
                    frame = pixel_mod.render_custom(data)
                    display.render(frame)
                    print(f"Rendered JSON pattern.")
            else:
                print(f"Invalid JSON pattern.", file=sys.stderr)
                sys.exit(1)
        except json.JSONDecodeError:
            print(f"Unknown pattern: {args.pattern}. Use 'list patterns'.", file=sys.stderr)
            sys.exit(1)


def cmd_state(args):
    client = _make_client(args)
    state = client.get_state()
    print(json.dumps(state, indent=2))


def cmd_clear(args):
    display = _make_display(args)
    display.clear()
    print("Display cleared.")


def cmd_list(args):
    if args.what == "animations":
        print("Animations: " + ", ".join(anim_mod.list_animations()))
    elif args.what == "scenes":
        print("Scenes: " + ", ".join(scenes_mod.list_scenes()))
    elif args.what == "patterns":
        print("Patterns: " + ", ".join(pixel_mod.list_patterns()))
        print("Animated: " + ", ".join(pixel_mod.list_animated_patterns()))
    elif args.what == "colors":
        print("Colors: " + ", ".join(sorted(NAMED_COLORS)))
    elif args.what == "fonts":
        from .font import available_chars
        print("Font chars: " + ", ".join(sorted(available_chars())))


def cmd_rainbow(args):
    display = _make_display(args)
    if args.brightness is not None:
        display.brightness(args.brightness)
    duration = _resolve_duration(args)
    frames = anim_mod.rainbow_chase()
    count = display.run_frames(frames, duration=duration, frame_interval=0.6,
                               on_stop_clear=not args.keep)
    print(f"Rainbow: {count} frames.")


def cmd_pulse(args):
    display = _make_display(args)
    color = parse_color(args.color)
    if args.brightness is not None:
        display.brightness(args.brightness)
    duration = _resolve_duration(args)
    frames = anim_mod.pulse(color=color)
    count = display.run_frames(frames, duration=duration, frame_interval=0.6,
                               on_stop_clear=not args.keep)
    print(f"Pulse: {count} frames.")


def cmd_segtest(args):
    client = _make_client(args)
    color = parse_color(args.color)
    print("=== Segment Control Test ===")
    print(f"Device: {client.sku} / {client.device}")
    print(f"Segments: {NUM_SEGMENTS} (0-{NUM_SEGMENTS - 1})")
    print(f"Test color: {args.color} (0x{color:06X} = {color})")
    print()
    print("1. Turning lamp on...")
    r = client.set_power(True)
    print(f"   {r}")
    time.sleep(0.5)
    print("2. Setting ALL segments to test color...")
    r = client.set_segments([color] * NUM_SEGMENTS)
    print(f"   {r}")
    time.sleep(2)
    print("3. Setting ALL segments to black...")
    r = client.set_segments([0] * NUM_SEGMENTS)
    print(f"   {r}")
    time.sleep(1)
    print("4. Setting segment 0 only...")
    frame = [0] * NUM_SEGMENTS
    frame[0] = color
    r = client.set_segments(frame)
    print(f"   {r}")
    time.sleep(2)
    print("5. Setting whole-lamp color via colorRgb...")
    r = client.set_color(color)
    print(f"   {r}")
    time.sleep(2)
    print("6. Turning lamp off...")
    r = client.set_power(False)
    print(f"   {r}")
    print()
    print("=== Done ===")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="govee_display",
        description="Govee H6022 Quantum Desk Lamp display engine.",
    )
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--sku", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--debug", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("power", help="Turn lamp on/off")
    p.add_argument("state", choices=["on", "off"])
    p.set_defaults(func=cmd_power)

    p = sub.add_parser("brightness", help="Set brightness 0-100")
    p.add_argument("value", type=int)
    p.set_defaults(func=cmd_brightness)

    p = sub.add_parser("color", help="Set whole-lamp color")
    p.add_argument("color", help="Color name, hex, or r,g,b")
    p.add_argument("--brightness", type=int, default=None)
    p.set_defaults(func=cmd_color)

    p = sub.add_parser("segments", help="Set individual segments")
    p.add_argument("specs", nargs="+", help="e.g. 0:red 1-5:blue 6-14:green")
    p.add_argument("--brightness", type=int, default=None)
    p.set_defaults(func=cmd_segments)

    p = sub.add_parser("text", help="Display text")
    p.add_argument("text")
    p.add_argument("--color", default="auto")
    p.add_argument("--mode", choices=["morse", "flash", "scroll", "segment_map"], default="morse")
    p.add_argument("--duration", type=float, default=None, help="Seconds (default: 10)")
    p.add_argument("--forever", action="store_true")
    p.add_argument("--speed", type=float, default=1.0, help="Speed multiplier (default: 1.0)")
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_text)

    p = sub.add_parser("animate", help="Run an animation")
    p.add_argument("name")
    p.add_argument("--color", default=None)
    p.add_argument("--duration", type=float, default=None, help="Seconds (default: 10)")
    p.add_argument("--forever", action="store_true")
    p.add_argument("--interval", type=float, default=None)
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--max-colors", type=int, default=6)
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_animate)

    p = sub.add_parser("scene", help="Run a scene preset")
    p.add_argument("name")
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_scene)

    p = sub.add_parser("pixel", help="Render pixel art")
    p.add_argument("pattern", help="Pattern name, bit string, or JSON")
    p.add_argument("--color", default="white")
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--duration", type=float, default=None)
    p.add_argument("--forever", action="store_true")
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_pixel)

    p = sub.add_parser("state", help="Get device state")
    p.set_defaults(func=cmd_state)

    p = sub.add_parser("clear", help="Clear display")
    p.set_defaults(func=cmd_clear)

    p = sub.add_parser("list", help="List available items")
    p.add_argument("what", choices=["animations", "scenes", "patterns", "colors", "fonts"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("rainbow", help="Quick rainbow animation")
    p.add_argument("--duration", type=float, default=None)
    p.add_argument("--forever", action="store_true")
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_rainbow)

    p = sub.add_parser("pulse", help="Quick pulse animation")
    p.add_argument("color")
    p.add_argument("--duration", type=float, default=None)
    p.add_argument("--forever", action="store_true")
    p.add_argument("--brightness", type=int, default=None)
    p.add_argument("--keep", action="store_true")
    p.set_defaults(func=cmd_pulse)

    p = sub.add_parser("segtest", help="Test segment control + print API responses")
    p.add_argument("--color", default="red")
    p.set_defaults(func=cmd_segtest)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except GoveeAPIError as exc:
        print(f"API error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
