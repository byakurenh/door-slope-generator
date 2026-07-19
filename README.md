# Door Slope Generator

A small Streamlit app that turns a single door sprite (PNG) into two "sloped" animation frames, used for the classic sliding-door open animation in RPG Maker.

Upload a door PNG, tweak the slope `step` value for each frame with a live, pixel-crisp preview, then export both frames as a ZIP.

## Features

- Upload a single door PNG as input
- Two independently adjustable `step` values (row-offset increment), one per output frame
- Live preview that updates instantly as you change the values, upscaled with nearest-neighbor scaling so small sprites stay sharp instead of blurry
- One-click **EXPORT** button that downloads both frames bundled in a single ZIP file

## Running locally

```bash
pip install -r requirements.txt
streamlit run door_slope_app.py
```

Then open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app.
3. Point it at this repo and set the main file to `door_slope_app.py`.
4. Streamlit Cloud will automatically install everything listed in `requirements.txt` (and `packages.txt`, if any system packages are ever added).

## Files

| File | Purpose |
|---|---|
| `door_slope_app.py` | The Streamlit app |
| `requirements.txt` | Python package dependencies |
| `packages.txt` | System-level (apt) dependencies — currently none needed |

## Credits

Inspired by Avery's a-door-able tutorial: https://forums.rpgmakerweb.com/threads/an-a-door-able-tutorial.156826/

Made by Byakuren
