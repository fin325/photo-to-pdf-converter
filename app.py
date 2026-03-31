import streamlit as st
from PIL import Image
import io
import base64

# ======================= GLASSMORPHISM + ФОН =======================
def set_glassmorphism_style(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()

        glass_css = f"""
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
            color: white !important;
            padding: 16px 40px !important;
            border-radius: 14px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
            transition: all 0.3s ease;
            width: 100% !important;
        }}

        .stFileUploader label:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.5) !important;
        }}

        /* Кнопка "Конвертировать" */
        .stButton > button {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            font-size: 1.25rem;
            font-weight: 700;
            padding: 16px 50px;
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45);
            transition: all 0.3s ease;
            width: 100%;
            height: 58px;
        }}

        .stButton > button:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(37, 99, 235, 0.55);
        }}

        /* Предпросмотр изображений */
        .stImage img {{
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }}
        
        .stImage img:hover {{
            transform: scale(1.03);
        }}
        </style>
        """
        st.markdown(glass_css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Файл фона не найден: {image_path}")

# ======================= ПРИМЕНЕНИЕ СТИЛЯ =======================
set_glassmorphism_style("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg")

# ======================= ПРИЛОЖЕНИЕ =======================
st.set_page_config(
    page_title="Foto to PDF",
    page_icon="📄",
    layout="centered"
)

# Заголовок
st.markdown('<h1 class="title">Foto to PDF</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">von Finevych A.</p>', unsafe_allow_html=True)

# Загрузчик файлов
uploaded