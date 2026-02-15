import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np
from io import BytesIO

st.set_page_config(page_title="AI Design OCR Editor", layout="centered")

st.title("🧠 AI Design Text Editor (OCR)")
st.write("Edit text inside AI-generated designs without regenerating the image")

uploaded = st.file_uploader(
    "Upload AI-generated image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:

    # --- SAFE IMAGE LOADING (Fixes UnidentifiedImageError) ---
    uploaded_bytes = uploaded.read()
    image = Image.open(BytesIO(uploaded_bytes)).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Image", use_container_width=True)

    # --- OCR ---
    with st.spinner("Detecting text..."):
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(img_np)

    detected_words = [r[1] for r in results]
    st.subheader("Detected text:")
    st.write(detected_words)

    target_text = st.text_input("Text to replace")
    new_text = st.text_input("New text")

    if st.button("Replace Text") and target_text and new_text:

        draw = ImageDraw.Draw(image)
        replaced = False

        for bbox, text, confidence in results:
            if target_text.lower() in text.lower():

                (tl, tr, br, bl) = bbox
                x1, y1 = map(int, tl)
                x2, y2 = map(int, br)

                # --- Sample surrounding background color ---
                crop = img_np[
                    max(0, y1-5):min(y2+5, img_np.shape[0]),
                    max(0, x1-5):min(x2+5, img_np.shape[1])
                ]

                avg_color = tuple(
                    np.mean(crop.reshape(-1, 3), axis=0).astype(int)
                )

                # Cover original text
                draw.rectangle([x1, y1, x2, y2], fill=avg_color)

                # Estimate font size based on bounding box height
                font_size = max(15, y2 - y1)

                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()

                # Write replacement text
                draw.text((x1, y1), new_text, fill=(255, 255, 255), font=font)

                replaced = True

        if replaced:
            st.success("Text replaced successfully!")
            st.image(image, caption="Edited Image", use_container_width=True)

            # --- FIXED DOWNLOAD (Real PNG File) ---
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            st.download_button(
                "Download Updated Image",
                data=buffer,
                file_name="edited_design.png",
                mime="image/png"
            )
        else:
            st.warning("Text not found. Check spelling or try another word.")
