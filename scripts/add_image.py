#!/usr/bin/env python3
"""Add (or update) one screensaver image in the AerialViews feed.

Given a freshly generated image, this:
  1. darkens the bottom 25% for overlay legibility,
  2. encodes it to a 30-second 1080p MP4,
  3. adds/updates the matching asset in entries.json — with the timeOfDay+scene
     tags the released app needs, so the video isn't silently filtered out.

Run once per new image, from the repo root:
    python scripts/add_image.py images/02_safari_animals.jpg
    python scripts/add_image.py images/02_safari_animals.jpg --desc "School hours"

The asset id and MP4 name come from the image filename (e.g. 02_safari_animals).
Re-running on an already-darkened image would darken it twice — pass --no-darken
to skip that step.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from darken_bottom import darken_bottom

REPO = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/rav-pawar/kids-tv-screensaver/main/videos/{name}.mp4"


def encode_mp4(image: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loop", "1", "-i", str(image), "-t", "30", "-r", "24",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                   "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-movflags", "+faststart", "-an", str(out),
        ],
        check=True,
    )


def upsert_entry(entries: Path, name: str, desc: str) -> int:
    data = json.loads(entries.read_text(encoding="utf-8")) if entries.exists() else {"assets": []}
    url = RAW.format(name=name)
    asset = {
        "id": name,
        "accessibilityLabel": desc,
        "timeOfDay": "day",
        "scene": "nature",
        "url-1080-SDR": url,
        "url-4K-SDR": url,
        "url-1080-H264": url,
    }
    assets = [a for a in data.get("assets", []) if a.get("id") != name]
    assets.append(asset)
    data["assets"] = assets
    entries.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return len(assets)


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("image", help="path to a freshly generated image, e.g. images/02_safari_animals.jpg")
    p.add_argument("--desc", default="School hours", help="overlay/metadata text (keep anonymized)")
    p.add_argument("--no-darken", action="store_true", help="skip the bottom-gradient step")
    a = p.parse_args()

    image = Path(a.image)
    if not image.is_absolute():
        image = (REPO / a.image).resolve()
    if not image.exists():
        sys.exit(f"Image not found: {image}")
    name = image.stem

    if not a.no_darken:
        darken_bottom(str(image), str(image), 0.25, 0.6)
        print(f"Darkened bottom 25% of {image.name}")

    mp4 = REPO / "videos" / f"{name}.mp4"
    encode_mp4(image, mp4)
    print(f"Encoded {mp4.relative_to(REPO)}")

    count = upsert_entry(REPO / "entries.json", name, a.desc)
    print(f"entries.json now has {count} asset(s). Commit & push to publish.")


if __name__ == "__main__":
    main()
