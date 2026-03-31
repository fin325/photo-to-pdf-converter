import streamlit as st
from PIL import Image
import io
import base64

# ======================= GLASSMORPHISM + ФОН =======================
def set_glassmorphism_style(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()

        glass_css = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Главный контейнер - эффект стекла */
        .main .block-container {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            padding: 35px 30px;
            max-width: 1050px;
            margin: 25px auto;
        }}

        /* Прозрачный header */
        header {{
            background: transparent !important;
        }}

        /* Заголовок */
        .title {{
            text-align: center;
            font-size: 3.4rem;
            font-weight: 700;
            background: linear-gradient(90deg, #1e40af, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.4rem;
            color: #1e3a8a;
            margin-bottom: 40px;
            font-weight: 500;
            opacity: 0.95;
        }}

        /* File Uploader - стеклянный стиль */
        .stFileUploader > section {{
            background: rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(12px);
            border: 2px dashed #60a5fa;
            border-radius: 18px;
            padding: 40px 20px;
        }}

        .stFileUploader label {{
            background: linear-gradient(135deg, #2563eb, #1e40af) !important;
            color: white