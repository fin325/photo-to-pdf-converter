import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Финальный блок стилей (Контейнер в цвет фона)
st.markdown("""
    <style>
    /* Фон всего приложения */
    .stApp {
        background: linear-gradient(135deg, #102a43 0%, #243b55 100%) !important;
    }

    /* Прозрачный контейнер (без заливки, только отступы) */
    .glass-container {
        background: transparent !important; /* Цвет как у фона */
        border: none !important;            /* Убираем рамку */
        padding: 10px;
        margin-top: 10px;
        text-align: center;
    }

    /* Заголовок */
    .main-title {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 25px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    /* СТИЛИЗАЦИЯ ЗАГРУЗЧИКА */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.05) !important; /* Легкий матовый налет */
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
    }
    
    div[data-testid="stFileUploader"] section div {
        display: none !important;
    }

    /* КНОПКА ЗАГРУЗКИ (Чистый текст) */
    div[data-testid="stFileUploader"] button {
        content: "📥 Загрузить фото";
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: transparent !important;
        font-size: 0 !important;
        height: 3.5em !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    div[data-testid="stFileUploader"] button::after {
        content: "📥 Отменить";
        font-size: 16px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* Кнопка "Создать PDF" */
    .stButton>button {
        background: #4A90E2 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3) !important;
        margin-top: 15px !important;
    }

    /* Тексты */
    .stMarkdown, p, span, label {
        color: #e0e0e0 !important;
    }

    /* Убираем лишние отступы Streamlit */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ИНТЕРФЕЙС (В прозрачном контейнере)
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "upload", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

st.markdown('</div>', unsafe_allow_html=True)

# 4. ЛОГИКА
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.write(f"✅ Выбрано фото: **{len(images)}**")
    
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Готово! PDF создан.")
        st.download_button("📥 СКАЧАТЬ PDF", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")
        
        # Предпросмотр
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600" style="border-radius:15px; border:none; margin-top:20px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Миниатюры
    st.markdown("---")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
