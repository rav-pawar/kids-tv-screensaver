#!/usr/bin/env python3
"""Darken the bottom strip of an image with a smooth gradient.

Improves legibility of AerialViews overlays (clock, weather, metadata) that sit
along the bottom of the screen. Run once on a fresh (bright) image.

Usage:
    python darken_bottom.py INPUT [OUTPUT] [--fraction 0.2] [--max-alpha 0.55]

If OUTPUT is omitted, the input is overwritten.
"""
import argparse
from PIL import Image


def darken_bottom(inp: str, outp: str, fraction: float, max_alpha: float) -> None:
    img = Image.open(inp).convert("RGBA")
    w, h = img.size
    strip = max(1, int(h * fraction))
    start = h - strip
    for y in range(start, h):
        t = (y - start) / strip          # 0 at top of strip, 1 at bottom edge
        alpha = int(255 * max_alpha * (t ** 1.4))  # eased so the top stays subtle
        img.alpha_composite(Image.new("RGBA", (w, 1), (0, 0, 0, alpha)), (0, y))
    img.convert("RGB").save(outp, quality=92)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input")
    p.add_argument("output", nargs="?")
    p.add_argument("--fraction", type=float, default=0.2, help="bottom portion to darken (0-1)")
    p.add_argument("--max-alpha", type=float, default=0.55, help="darkness at the very bottom (0-1)")
    a = p.parse_args()
    darken_bottom(a.input, a.output or a.input, a.fraction, a.max_alpha)
    print(f"Darkened bottom {a.fraction:.0%} -> {a.output or a.input}")
