import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np
from io import BytesIO

st.set_page_config(page_title="AI Design Editor", layout="centered")

# ---------- Modern Creative UI Styling ----------
st.markdown("""
<style>
.stApp {
    background: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 2rem;
}

.stButton>button {
    background-color: #111827;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #374151;
    color: white;
}

.stFileUploader {
    background-color: #ffffff;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ---------- Clean Title ----------
st.markdown("<h1>AI Design Editor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Edit text inside AI-generated flyers and designs without regenerating the image.</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------- Upload ----------
uploaded = st.file_uploader(
    "Upload AI-generated image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:

    # Safe loading
    uploaded_bytes = uploaded.read()
    image = Image.open(BytesIO(uploaded_bytes)).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Design", use_container_width=True)

    # OCR detection
    with st.spinner("Detecting text in design..."):
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(img_np)

    detected_words = [r[1] for r in results]

    if detected_words:
        st.write("Detected text:", detected_words)
    else:
        st.warning("No text detected in image.")

    st.markdown("### Replace Text")

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

                # --- Background Sampling ---
                crop = img_np[
                    max(0, y1-5):min(y2+5, img_np.shape[0]),
                    max(0, x1-5):min(x2+5, img_np.shape[1])
                ]

                avg_bg_color = tuple(
                    np.mean(crop.reshape(-1, 3), axis=0).astype(int)
                )

                # --- Sample Original Text Color ---
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                text_color = tuple(img_np[center_y, center_x])

                # Cover old text
                draw.rectangle([x1, y1, x2, y2], fill=avg_bg_color)

                # Smart font scaling
                font_size = box_height

                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()

                # Resize font to match original width
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

                # Center alignment
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
            st.warning("Text not found. Please check spelling.")
