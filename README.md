# TV Screensaver Images

A small set of cheerful, kid-friendly illustrations used as a TV screensaver via
[AerialViews](https://github.com/theothernt/AerialViews) on Android / Google / Fire TV.

The images display daily school timings so the family can see them at a glance on the TV.

## How it's used

AerialViews reads a **custom media feed** — a CSV list of image URLs. Point AerialViews at
the raw URL of [`media_list.csv`](media_list.csv) in this repo:

```
https://raw.githubusercontent.com/rav-pawar/kids-tv-screensaver/main/media_list.csv
```

In AerialViews: **Settings → Custom feed → Custom Media URLs** → paste the URL above.

## Contents

| File | Purpose |
|------|---------|
| `images/` | The screensaver images (1920×1080 PNG). |
| `media_list.csv` | The feed AerialViews reads (`url,description` per line). |
| `schedule.json` | The timings shown on the images (source of truth). |

## Updating

Edit or replace an image in `images/`, keep `media_list.csv` in sync, and push.
AerialViews picks up changes on its next refresh.
