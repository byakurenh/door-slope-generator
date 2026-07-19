import io
import zipfile

import streamlit as st
from PIL import Image

# Page configuration setup
st.set_page_config(page_title="Door Slope Generator", layout="centered")

# Top header layout to push the credit line and About button to the right edge
col_title, col_about = st.columns([6, 1])

with col_title:
    st.title("🚪 Door Slope Generator")

with col_about:
    st.markdown(
        "<div style='text-align: right; font-size: 0.8rem; color: #808495; margin-top: 10px; margin-bottom: 4px;'>Developed by Byakuren</div>",
        unsafe_allow_html=True,
    )
    with st.popover("ℹ️ About", use_container_width=True):
        st.markdown(
            "Inspired by Avery's a-door-able tutorial: "
            "https://forums.rpgmakerweb.com/threads/an-a-door-able-tutorial.156826/"
        )
        st.markdown("Made by Byakuren")

st.caption(
    "Upload a door PNG file to generate two sloped frames (Outputs) with a live preview. "
    "Adjust the step value for each frame independently, then download both as a ZIP."
)


def make_slope(img: Image.Image, step: int) -> Image.Image:
    """
    Creates a 'sloped door' frame from the input image.
    step = the row-offset increment described in the reference diagram
           ("offset every Npx"): step=3 for the classic '38' frame,
           step=1 for the classic '23' frame.
    """
    w, h = img.size
    src = img.convert("RGBA")
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src_px = src.load()
    out_px = out.load()

    # How much of the door's width stays visible after the slope is applied,
    # and how far (k) the remaining columns are sampled from on the right.
    visible_width = (w * step) // (step + 1)
    k = w - visible_width

    for x in range(visible_width):
        # The vertical shift grows by 1 every `step` pixels, starting at 1.
        shift = 1 if x == 0 else ((x - 1) // step) + 1
        # The leftmost column stays anchored to the original left edge;
        # every other column samples from further right (x + k).
        source_x = 0 if x == 0 else x + k
        for y in range(h):
            source_y = y + shift
            if source_y < h and source_x < w:
                out_px[x, y] = src_px[source_x, source_y]
            # else: leave transparent
    return out


def crisp_preview(img: Image.Image, target_size: int = 200) -> Image.Image:
    """
    Upscales a small image using nearest-neighbor interpolation so the preview
    stays sharp (no blur), instead of stretching it with smooth interpolation.
    The scale factor is always a whole number to keep pixel edges crisp.
    """
    w, h = img.size
    longest_side = max(w, h)
    # Whole-number scale factor only, so pixels stay sharp instead of blurring
    scale = max(1, target_size // longest_side)
    return img.resize((w * scale, h * scale), Image.NEAREST)


uploaded_file = st.file_uploader("Choose a door PNG file", type=["png"])

if uploaded_file is not None:
    try:
        original_img = Image.open(io.BytesIO(uploaded_file.read())).convert("RGBA")
        w, h = original_img.size

        st.image(crisp_preview(original_img), caption=f"Original door (Input) - {w}x{h}px")

        st.write("---")
        st.subheader("Step Settings for Each Frame")
        st.caption(
            "'step' is the row-offset increment used by the algorithm "
            "(not a pixel-width label). step=3 reproduces the classic '38' look, "
            "step=1 reproduces the classic '23' look."
        )

        col1, col2 = st.columns(2)

        with col1:
            step1 = st.number_input(
                "Step - Frame 1",
                min_value=1,
                max_value=50,
                value=3,
                step=1,
            )

        with col2:
            step2 = st.number_input(
                "Step - Frame 2",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
            )

        frame1 = make_slope(original_img, step=int(step1))
        frame2 = make_slope(original_img, step=int(step2))

        st.write("---")
        st.subheader("Live Preview")

        preview_col1, preview_col2 = st.columns(2)
        with preview_col1:
            st.image(crisp_preview(frame1), caption=f"Frame 1 (step {int(step1)})")
        with preview_col2:
            st.image(crisp_preview(frame2), caption=f"Frame 2 (step {int(step2)})")

        st.write("---")

        # Build ZIP in memory for export
        original_name = uploaded_file.name.rsplit(".", 1)[0]
        buf1 = io.BytesIO()
        frame1.save(buf1, format="PNG")
        buf2 = io.BytesIO()
        frame2.save(buf2, format="PNG")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{original_name}_step{int(step1)}.png", buf1.getvalue())
            zf.writestr(f"{original_name}_step{int(step2)}.png", buf2.getvalue())

        st.download_button(
            label="EXPORT - Download ZIP with both files",
            data=zip_buffer.getvalue(),
            file_name=f"{original_name}_slopes.zip",
            mime="application/zip",
            type="primary",
        )

    except Exception as read_err:
        st.error(f"Failed to read the file. Make sure it is a valid PNG. Details: {read_err}")