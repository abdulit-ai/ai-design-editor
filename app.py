import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="AI Design Text Editor", layout="centered")

st.title("🖼️ AI Design Text Editor")
st.write("Edit text on AI-generated designs (flyers, posters, banners)")

uploaded = st.file_uploader(
    "Upload AI-generated design (PNG/JPG)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGBA")
    draw = ImageDraw.Draw(image)

    st.subheader("Text Replacement")

    old_text = st.text_input("Original text (for reference only)", "Zahra")
    new_text = st.text_input("New text", "Sofra")

    col1, col2 = st.columns(2)
    with col1:
        x = st.slider("Text X position", 0, image.width, int(image.width * 0.2))
        y = st.slider("Text Y position", 0, image.height, int(image.height * 0.1))
    with col2:
        font_size = st.slider("Font size", 20, 150, 60)

    bg_color = st.color_picker("Background cover color", "#000000")
    text_color = st.color_picker("Text color", "#FFFFFF")

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Cover old text area (simple rectangle)
    padding = 10
    text_width, text_height = draw.textsize(old_text, font=font)
    draw.rectangle(
        [
            x - padding,
            y - padding,
            x + text_width + padding,
            y + text_height + padding
        ],
        fill=bg_color
    )

    # Draw new text
    draw.text((x, y), new_text, fill=text_color, font=font)

    st.image(image, caption="Edited Design", use_container_width=True)

    st.download_button(
        "Download Updated Design",
        data=image.tobytes(),
        file_name="edited_design.png",
        mime="image/png"
    )
