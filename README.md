<div align="center">

# 🌈 Govee Display

### Custom display controller for the Govee H6022 Quantum Desk Lamp

Render **pixel art**, **scrolling text**, and **animated scenes** on your lamp's 15 LED segments via the Govee Cloud API v2.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dependencies: None](https://img.shields.io/badge/dependencies-zero-green.svg)](requirements.txt)
[![API: Govee v2](https://img.shields.io/badge/API-Govee%20v2-orange.svg)](https://developer.govee.com)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Pixel Art** | Render 48+ built-in patterns (heart, smiley, invader, bitcoin…) or custom bit strings on the 15-segment grid |
| **Text Scrolling** | Spell out words using a 3×5 pixel font — flash letters one at a time or scroll them as a marquee |
| **Animated Scenes** | 20 animations: rainbow chase, fire flicker, matrix rain, ocean waves, aurora, lightning, heartbeat & more |
| **Scene Presets** | 15 ready-to-run scenes with tuned colors, brightness, and timing |
| **Segment Calibration** | Light each segment 0–14 individually to map your lamp's physical layout |
| **Dry-Run Preview** | Preview any animation as ANSI-colored art in your terminal — no lamp or API key needed |
| **Zero Dependencies** | Pure Python standard library — no `pip install` required |
| **Rate-Limited** | Token-bucket limiter respects the 2 req/sec API cap with burst support and automatic retries |

---

## 📦 Installation

### Option A — Run directly (no install)

```bash
git clone https://github.com/donewiththedollar/my-govee.git
cd my-govee
python3 govee_display.py --help
```

### Option B — Install as a package

```bash
git clone https://github.com/donewiththedollar/my-govee.git
cd my-govee
pip install .
govee-display --help
```

> **No external dependencies.** Works with Python 3.8+ using only the standard library.

---

## 🔑 Configuration

You need a **Govee API key** and your lamp's **device address**.

### 1. Get an API key

1. Visit the [Govee Developer Portal](https://developer.govee.com)
2. Create an application
3. Copy your API key

### 2. Find your device address

Use the Govee API to list your devices, or find the BLE address in the **Govee Home** app under your lamp's settings.

### 3. Set environment variables

```bash
export GOVEE_API_KEY="your-api-key-here"
export GOVEE_DEVICE="AA:BB:CC:DD:EE:FF"
```

Or create a `.env` file (copy `.env.example`):

```bash
cp .env.example .env
# Edit .env with your values, then:
source .env
```

You can also pass credentials per-command:

```bash
python3 govee_display.py --api-key YOUR_KEY --device AA:BB:CC:DD:EE:FF text BTC
```

---

## 🚀 Quick Start

```bash
# Flash the word "BTC" on the lamp
python3 govee_display.py text BTC

# Scroll text like a marquee
python3 govee_display.py text HELLO --mode scroll

# Run the rainbow chase animation for 30 seconds
python3 govee_display.py animate rainbow --duration 30

# Display a pixel art heart in red
python3 govee_display.py pixel heart --color red

# Run the bitcoin scene preset
python3 govee_display.py scene bitcoin

# Preview without a lamp (no API key needed!)
python3 govee_display.py --dry-run animate fire --duration 10
```

---

## 🖥️ Segment Layout

The H6022 has **15 individually-addressable LED segments**. This tool maps them to a **3×5 grid** (3 columns × 5 rows) so letters and pixel art are recognizable:

```
  Col 0   Col 1   Col 2
┌────────┬────────┬────────┐
│  seg 0 │  seg 1 │  seg 2 │  Row 0 (top)
├────────┼────────┼────────┤
│  seg 3 │  seg 4 │  seg 5 │  Row 1
├────────┼────────┼────────┤
│  seg 6 │  seg 7 │  seg 8 │  Row 2
├────────┼────────┼────────┤
│  seg 9 │ seg 10 │ seg 11 │  Row 3
├────────┼────────┼────────┤
│ seg 12 │ seg 13 │ seg 14 │  Row 4 (bottom)
└────────┴────────┴────────┘
```

> **Tip:** Run `python3 govee_display.py test` to light each segment one at a time and verify the mapping matches your lamp's physical layout.

---

## 🔤 Pixel Font

A compact **3×5 bitmap font** supports the full alphabet, digits, and common symbols:

```
A   B   C   D   E   F   G   H   I   J   K   L   M
.#. ##. .## ##. ### ### .## #.# ### ### #.# #.. #.#
#.# #.# #.. #.# #.. #.. #.. #.# .#. ..# #.# #.. ###
#.# #.# #.. #.# ##. ##. #.# ### .#. ..# #.# #.. ###
### ##. #.. #.# #.. #.. #.# #.# .#. #.# ##. #.. #.#
#.# #.# .## ##. ### #.. .## #.# ### .## #.# ### #.#

N   O   P   Q   R   S   T   U   V   W   X   Y   Z
#.# .#. ##. .#. ##. .## ### #.# #.# #.# #.# #.# ###
##. #.# #.# #.# #.# #.. .#. #.# #.# #.# #.# .#. ..#
#.# #.# #.# #.# #.# .#. .#. #.# #.# .#. .#. .#. .#.
#.# #.# #.. .#. #.# ..# .#. .#. .#. .#. #.# .#. #..
#.# .#. #.. .#. #.# ##. .#. .#. .#. .#. #.# .#. ###
```

---

## 📋 Command Reference

```
govee_display.py [global options] <command> [command options]
```

### Global Options

| Option | Description |
|--------|-------------|
| `--api-key KEY` | Govee API key (or env: `GOVEE_API_KEY`) |
| `--device ADDR` | Device BLE address (or env: `GOVEE_DEVICE`) |
| `--sku SKU` | Device model (default: `H6022`) |
| `--dry-run` | Preview in terminal without API calls |

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `text` | Display text (flash or scroll) | `text BTC --color bitcoin` |
| `animate` | Run an animation | `animate rainbow --duration 30` |
| `pixel` | Render a pixel art pattern | `pixel heart --color red` |
| `scene` | Run a scene preset | `scene matrix` |
| `test` | Calibrate segments (light each in sequence) | `test --interval 0.5` |
| `segments` | Print the segment-to-grid mapping | `segments` |
| `color` | Set whole-lamp color | `color blue` |
| `brightness` | Set brightness (0–100) | `brightness 75` |
| `power` | Turn lamp on/off | `power on` |
| `clear` | Turn all segments off | `clear` |
| `state` | Query device state | `state` |
| `list` | List animations/scenes/patterns/colors | `list scenes` |

### Common Command Options

| Option | Applies to | Description |
|--------|-----------|-------------|
| `--color NAME` | text, animate, pixel, color | Color name, hex (`#FF0000`), or `bitcoin` |
| `--brightness N` | most | Set brightness 0–100 |
| `--duration SEC` | text, animate, scene | Stop after N seconds (default: runs forever) |
| `--interval SEC` | text, animate, scene, test | Seconds per frame |
| `--keep` | text, animate, scene | Don't clear display on exit |
| `--mode flash\|scroll` | text | Flash = one letter at a time, scroll = marquee |
| `--no-blank` | text | Skip blank frame between letters |

---

## 🎬 Animations

20 built-in animations. Run with `animate <name>`:

| Animation | Description |
|-----------|-------------|
| `rainbow` / `rainbow_chase` | Rainbow colors chasing along segments |
| `wave` / `color_wave` | Sine wave of a single color |
| `pulse` | Whole-display color pulse |
| `fire` / `fire_flicker` | Random fire flicker with warm tones |
| `matrix` / `matrix_rain` | Matrix digital rain with trailing tails |
| `ocean` / `ocean_wave` | Calm blue ocean waves |
| `aurora` / `aurora_chase` | Aurora borealis in green/purple/teal |
| `lightning` / `lightning_flash` | Lightning storm with random flashes |
| `heartbeat` | Two-pulse heartbeat rhythm |
| `chase` | Comet with fading tail |
| `breathe` | Slow breathing effect |
| `color_cycle` | Hue cycle across the whole display |
| `twinkle` | Random twinkling stars |
| `gradient` / `gradient_shift` | Shifting rainbow gradient |
| `police` | Alternating red and blue lights |
| `candle` | Warm candle flicker |
| `strobe` | Fast strobe light |
| `noise` / `static` | TV static noise |
| `sunrise` | Gradual sunrise/sunset |
| `bounce` / `color_bounce` | Ball of light bouncing back and forth |

```bash
python3 govee_display.py animate fire --color orange --duration 60
python3 govee_display.py animate matrix --color "#00FF41"
python3 govee_display.py --dry-run animate aurora --duration 10 --interval 0.3
```

---

## 🎨 Scene Presets

15 ready-to-run scenes with tuned colors and timing. Run with `scene <name>`:

| Scene | Animation | Color | Description |
|-------|-----------|-------|-------------|
| `bitcoin` | pulse | bitcoin orange | Bitcoin orange pulse |
| `matrix` | matrix_rain | matrix green | Matrix digital rain |
| `fire` | fire_flicker | fire orange-red | Fire flicker |
| `ocean` | ocean_wave | ocean blue | Ocean wave |
| `aurora` | aurora_chase | aurora green | Aurora chase |
| `rainbow` | rainbow_chase | spectrum | Rainbow chase |
| `lightning` | lightning_flash | white | Lightning flash |
| `heartbeat` | heartbeat | crimson | Heartbeat |
| `police` | police | red/blue | Police lights |
| `candle` | candle | orange | Candle flicker |
| `strobe` | strobe | white | Strobe light |
| `sunrise` | sunrise | orange | Sunrise / sunset |
| `bounce` | color_bounce | cyan | Bouncing light |
| `twinkle` | twinkle | white | Twinkling stars |
| `breathe` | breathe | purple | Breathing purple |

```bash
python3 govee_display.py scene bitcoin --duration 120
python3 govee_display.py scene matrix
```

---

## 🖼️ Pixel Art Patterns

48 built-in patterns. Run with `pixel <name>`:

```
heart  smiley  frown  arrow_up  arrow_down  arrow_left  arrow_right
diamond  cross  checker  border  x  t  hbar  vbar  corners  top  bottom
invader  ghost  note  star  tree  house  cup  full  empty  stairs
zigzag  circle  dot  exclaim  question  plus  minus  equals  triangle
hourglass  bowtie  chevron  bracket  pillars  arch  tent  mountain
wave  spiral  bitcoin
```

You can also pass a raw **bit string** (15 characters, `1` = on, `0` = off):

```bash
# Light segments 0, 2, 4, 6, 8, 10, 12, 14
python3 govee_display.py pixel "101010101010101" --color cyan
```

---

## 🎨 Colors

100+ named colors are available. Use any of them with `--color`:

```
red  green  blue  white  black  yellow  cyan  magenta  orange  purple
pink  lime  teal  navy  gold  bitcoin  matrix  fire  ocean  aurora
crimson  emerald  sapphire  ruby  ice  coral  mint  sky  rose  neon
...and many more (run `list colors` to see all)
```

Hex colors also work: `--color "#F7931A"` or `--color F7931A`.

---

## 🛠️ Programmatic API

You can use the library directly in your own Python scripts:

```python
from govee.client import GoveeClient
from govee.display import GoveeDisplay
from govee import animations, text, pixel

# Create a client (reads GOVEE_API_KEY and GOVEE_DEVICE from env)
client = GoveeClient()
display = GoveeDisplay(client)

# Set brightness
display.brightness(80)

# Flash text
frames = text.flash_frames("HELLO", color=0x00FF00)
display.run_frames(frames, duration=10, frame_interval=0.8)

# Run an animation
frames = animations.rainbow_chase()
display.run_frames(frames, duration=30, frame_interval=0.6)

# Render pixel art
display.render(pixel.render_pattern("heart", 0xFF0000))

# Clear when done
display.clear()
```

### Custom Animations

Any generator that yields lists of 15 RGB integers works:

```python
from govee.display import GoveeDisplay
from govee.client import GoveeClient
from govee.colors import rgb_to_int

def my_animation():
    while True:
        for i in range(15):
            frame = [0] * 15
            frame[i] = rgb_to_int(255, 0, 0)  # red dot moving
            yield frame

display = GoveeDisplay(GoveeClient())
display.run_frames(my_animation(), duration=30, frame_interval=0.4)
```

---

## ⚙️ How It Works

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Your Script │────▶│ GoveeDisplay  │────▶│   GoveeClient    │
│  / CLI       │     │  (15-segment) │     │  (rate-limited)  │
└──────────────┘     └───────────────┘     └────────┬─────────┘
                                                      │
                                            ┌─────────▼─────────┐
                                            │  Govee Cloud API   │
                                            │  v2 (HTTPS POST)   │
                                            └─────────┬─────────┘
                                                      │
                                            ┌─────────▼─────────┐
                                            │  H6022 Desk Lamp   │
                                            │  (15 LED segments)  │
                                            └───────────────────┘
```

- **Frame** = a list of 15 RGB integers (one per segment)
- Segments are **grouped by color** so a full frame is a single API call
- The **token-bucket rate limiter** (2 req/sec, burst 6) prevents API throttling
- Failed requests (429, 5xx) are **automatically retried** with backoff

---

## 🔧 Troubleshooting

<details>
<summary><b>Configuration error: API key not found</b></summary>

Set the environment variable:
```bash
export GOVEE_API_KEY="your-key"
```
Or pass it directly: `--api-key your-key`
</details>

<details>
<summary><b>Configuration error: device address not found</b></summary>

Set the environment variable:
```bash
export GOVEE_DEVICE="AA:BB:CC:DD:EE:FF"
```
Find your device address in the Govee Home app or via the API device list endpoint.
</details>

<details>
<summary><b>HTTP 429: Rate limited</b></summary>

The built-in rate limiter should prevent this, but if you're running multiple instances, reduce your frame rate with `--interval 1.0` or higher. The API allows 2 requests/sec per device.
</details>

<details>
<summary><b>Animation looks wrong / segments are scrambled</b></summary>

The 3×5 grid mapping may not match your lamp's physical segment order. Run:
```bash
python3 govee_display.py test
```
This lights each segment 0–14 in sequence so you can see the actual physical layout.
</details>

<details>
<summary><b>Want to preview without a lamp?</b></summary>

Use `--dry-run` to render frames as ANSI-colored art in your terminal:
```bash
python3 govee_display.py --dry-run animate rainbow --duration 10
```
No API key or device required.
</details>

---

## 📁 Project Structure

```
my-govee/
├── govee_display.py      # CLI entry point
├── govee/
│   ├── __init__.py       # Package init
│   ├── client.py          # Govee Cloud API v2 client (rate limiting, retries)
│   ├── display.py         # 15-segment display controller + preview
│   ├── colors.py          # Color utilities (HSV, RGB, hex, 100+ named colors)
│   ├── font.py            # 3×5 pixel font (A-Z, 0-9, symbols)
│   ├── text.py            # Text flash & scroll rendering
│   ├── pixel.py           # 48 pixel art patterns
│   ├── animations.py      # 20 animation generators
│   ├── scenes.py          # 15 scene presets
│   └── cli.py             # argparse CLI with all commands
├── pyproject.toml         # Package metadata & install config
├── .env.example           # Environment variable template
├── requirements.txt       # (empty — zero dependencies)
├── LICENSE                # MIT
└── README.md              # This file
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new animations, scenes, or pixel patterns
- Improve the font or add alternate layouts
- Fix bugs or improve documentation

```bash
git clone https://github.com/donewiththedollar/my-govee.git
cd my-govee
# Make your changes
python3 govee_display.py --dry-run animate <your-animation> --duration 5
```

---

## 📜 License

[MIT](LICENSE) — free to use, modify, and distribute.

---

<div align="center">

**Built for the [Govee H6022 Quantum Desk Lamp](https://www.govee.com)**

⭐ If this project helped you, consider giving it a star!

</div>
