# TV Screensaver Images

A small set of cheerful, kid-friendly illustrations used as a TV screensaver via
[AerialViews](https://github.com/theothernt/AerialViews) on Android / Google / Fire TV.

The images display daily school timings so the family can see them at a glance on the TV.

## How it's used

AerialViews reads a **custom feed**. Point AerialViews at the raw URL of
[`entries.json`](entries.json) in this repo:

```
https://raw.githubusercontent.com/rav-pawar/kids-tv-screensaver/main/entries.json
```

In AerialViews: **Settings → Sources → Custom feeds → enable → Feed URLs** → paste the URL above.

### Why a video feed (entries.json) and not a CSV of images?

AerialViews can show remote *photos* via a CSV feed, but **CSV support is only on the app's
`master` branch — it is not in any released version (≤ v1.8.2).** On a released build, a `.csv`
feed URL fails with *"URL does not contain a valid manifest.json / No valid URLs found."*

The released app **does** support the `entries.json` video feed (since v1.8.0). So each schedule
image is encoded as a short static-image **MP4** and listed in `entries.json`. This works on the
current app and still keeps everything hosted on GitHub.

When a release with CSV support ships, [`media_list.csv`](media_list.csv) can be used instead.

## Contents

| File | Purpose |
|------|---------|
| `entries.json` | The feed AerialViews reads now (video format). |
| `videos/` | Static-image MP4s referenced by `entries.json`. |
| `images/` | Source images (used to build the MP4s; and for CSV later). |
| `media_list.csv` | Image feed for when the app's CSV support is released. |
| `schedule.json` | The timings shown on the images (source of truth). |

## Updating / adding images

**Add a new theme image** — generate it (bottom 25% kept clear of text), save to `images/`, then:

```sh
python scripts/add_image.py images/NN_name.jpg
git add -A && git commit -m "Add NN_name screensaver" && git push
```

`add_image.py` darkens the bottom strip, encodes the MP4, and adds the asset to `entries.json`
with the `timeOfDay`/`scene` tags the released app needs. AerialViews rotates through every asset,
so you can add as many as you like. Allow ~5 min for the raw-URL cache after pushing.

**Change an existing image:** replace it in `images/`, run the same command (add `--no-darken`
if the file is already darkened), commit, and push.

Low-level encode (if doing it by hand):

```sh
ffmpeg -y -loop 1 -i images/NN_name.jpg -t 30 -r 24 -c:v libx264 -pix_fmt yuv420p \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -movflags +faststart -an videos/NN_name.mp4
```
