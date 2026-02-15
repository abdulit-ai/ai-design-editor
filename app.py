import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import easyocr
import numpy as np
from io import BytesIO

st.set_page_config(page_title="AI Design Editor", layout="centered")

# ---------- Creative UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
}
.block-container {
    background-color: white;
    padding: 2.5rem;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #111827;
}
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 2rem;
}
.stButton>button {
    background-color: #111827;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #374151;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1>AI Design Editor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Edit text inside AI-generated flyers without regenerating the image.</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------- Cached OCR Loader ----------
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'], gpu=False)

# ---------- Upload ----------
uploaded = st.file_uploader(
    "Upload AI-generated image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:

    uploaded_bytes = uploaded.read()
    image = Image.open(BytesIO(uploaded_bytes)).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Design", use_container_width=True)

    st.info("Loading OCR engine (first run may take 30–60 seconds)...")
    reader = load_ocr()

    with st.spinner("Detecting text in image..."):
        results = reader.readtext(img_np)

    st.write("Detected text:", [r[1] for r in results])

    col1, col2 = st.columns(2)
    with col1:
        target_text = st.text_input("Text to replace")
    with col2:
        new_text = st.text_input("New text")

    if st.button("Apply Changes") and target_text and new_text:

        draw = ImageDraw.Draw(image)
        replaced = False

        for bbox, text, confidence in results:
            if target_text.lower() in text.lower():

                (tl, tr, br, bl) = bbox
                x1, y1 = map(int, tl)
                x2, y2 = map(int, br)

                box_width = x2 - x1
                box_height = y2 - y1

                # ---- Blur background instead of rectangle ----
                region = image.crop((x1, y1, x2, y2))
                blurred = region.filter(ImageFilter.GaussianBlur(radius=8))
                image.paste(blurred, (x1, y1))

                # ---- Sample original text color ----
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                text_color = tuple(img_np[center_y, center_x])

                # ---- Smart font scaling ----
                font_size = box_height
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()

                while True:
                    bbox_text = draw.textbbox((0, 0), new_text, font=font)
                    text_width = bbox_text[2] - bbox_text[0]

                    if text_width <= box_width or font_size <= 10:
                        break

                    font_size -= 2
                    try:
                        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                    except:
                        font = ImageFont.load_default()

                text_x = x1 + (box_width - text_width) / 2
                text_y = y1 + (box_height - font_size) / 2

                draw.text((text_x, text_y), new_text, fill=text_color, font=font)

                replaced = True

        if replaced:
            st.success("Design updated successfully.")
            st.image(image, caption="Updated Design", use_container_width=True)

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            st.download_button(
                "Download Updated Design",
                data=buffer,
                file_name="edited_design.png",
                mime="image/png"
            )
        else:
            st.warning("Text not found.")
