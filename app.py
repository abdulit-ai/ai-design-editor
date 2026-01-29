import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np

st.set_page_config(page_title="AI Design OCR Editor", layout="centered")

st.title("🧠 AI Design Text Editor (OCR)")
st.write("Edit text inside AI-generated designs using OCR")

uploaded = st.file_uploader(
    "Upload AI-generated image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    img_np = np.array(image)

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(img_np)

    st.subheader("Detected Text")
    detected_texts = [res[1] for res in results]
    st.write(detected_texts)

    target_text = st.text_input("Text to replace", "Zahra")
    new_text = st.text_input("New text", "Sofra")

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    replaced = False

    for bbox, text, confidence in results:
        if target_text.lower() in text.lower():
            (top_left, top_right, bottom_right, bottom_left) = bbox

            x1, y1 = map(int, top_left)
            x2, y2 = map(int, bottom_right)

            # cover old text
            draw.rectangle([x1, y1, x2, y2], fill="black")

            # write new text
            draw.text((x1, y1), new_text, fill="white", font=font)

            replaced = True

    if replaced:
        st.image(image, caption="Edited Design", use_container_width=True)

        st.download_button(
            "Download Updated Design",
            data=image.tobytes(),
            file_name="ocr_edited_design.png",
            mime="image/png"
        )
    else:
        st.warning("Target text not found. Try adjusting the text.")
