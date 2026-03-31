import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# ОБНОВЛЕННЫЙ СТИЛЬ (Более мощные селекторы)
st.markdown("""
    <style>
    /* Фон и общие настройки */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    /* Заголовок */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }

    /* МАТОВАЯ ПАНЕЛЬ */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* РАБОТА С КНОПКОЙ ЗАГРУЗКИ (BROWSE FILES) */
    /* 1. Делаем всю зону загрузки матовой */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    /* 2. Прячем стандартный текст внутри кнопки */
    div[data-testid="stFileUploader"] button div[data-testid="stMarkdownContainer"] p {
        display: none !important;
    }

    /* 3. Вставляем свой текст "Загрузить файлы" */
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        color: white !important;
        font-weight: bold;
    }

    /* 4. Стили самой кнопки внутри загрузчика */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        width: 100% !important;
    }

    /* КНОПКА КОНВЕРТАЦИИ */
    .stButton>button {
        background: rgba(74, 144, 226, 0.4) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px;
        height: 3.8em;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: rgba(74, 144, 226, 0.6) !important;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.5);
    }

    /* Тексты */
    p, span, label {
        color: #f0f0f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Контейнер
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Загрузить файл", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with col2:
    st.write("###") # Выравнивание
    convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)
st.markdown('</div>', unsafe_allow_html=True)

# Логика (кратко)
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Готово!")
        st.download_button("📥 СКАЧАТЬ PDF", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")
        
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="500" style="border-radius:15px; margin-top:15px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Галерея
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
