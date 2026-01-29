import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="AI Design Editor", layout="centered")

st.title("🎨 AI Design Editor")
st.write("Upload an AI-generated design and edit text on it")

uploaded = st.file_uploader("Upload design image", type=["png", "jpg", "jpeg"])

if uploaded:
    image = Image.open(uploaded).convert("RGBA")
    draw = ImageDraw.Draw(image)

    text = st.text_input("Edit text")
    x = st.slider("Text X position", 0, image.width)
    y = st.slider("Text Y position", 0, image.height)
    size = st.slider("Font size", 10, 120, 40)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except:
        font = ImageFont.load_default()

    if text:
        draw.text((x, y), text, fill="white", font=font)

    st.image(image, caption="Edited Design", use_container_width=True)

    st.download_button(
        "Download design",
        data=image.tobytes(),
        file_name="edited_design.png",
        mime="image/png"
    )
