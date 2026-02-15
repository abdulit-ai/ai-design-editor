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
    border: 1px solid #e5e7eb
