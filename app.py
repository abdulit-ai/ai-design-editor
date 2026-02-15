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

# ---------- Upload ----------
uploaded = st.file_uploader(
    "Upload AI-generated image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:

    uploaded_bytes = uploaded.read()
    image = Image.open(BytesIO(uploaded_bytes)).convert("RGB")
