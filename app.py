import streamlit as st
from PIL import Image
import io
import base64

# Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# УЛУЧШЕННЫЙ CSS
st.markdown("""
    <style>
    /* 1. Общий фон приложения */
    .stApp {
        background: linear-gradient(135deg, #102a43 0%, #243b55 100%) !important;
    }

    /* 2. Матовая панель (теперь заголовок ВНУТРИ неё) */
    .glass-container {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin-top: 20px;
    }

    /* 3. Текст заголовка */
    .main-title {
        font-size: 26px;
        font-weight: 800;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 20px;
    }

    /* 4. Настройка загрузчика (делаем его прозрачным) */
    div[data-testid="stFileUploader"] {
        background-color: transparent !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Делаем фон внутри загрузчика тоже прозрачным */
    div[data-testid="stFileUploader"] section {
        background-color: transparent !important;
        color: white !important;
    }

    /* 5. Кнопка "Загрузить фото" - делаем текст ЯРКИМ */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: white !important;
    }
    
    /* Хак для замены текста на белый */
    div[data-testid="stFileUploader"] button div[data-testid="stMarkdownContainer"] p {
        display: none !important;
    }
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        color: #FFFFFF !important; /* Чисто белый цвет */
        font-weight: bold;
        font-size: 16px;
    }

    /* 6. Кнопка Создать PDF */
    .stButton>button {
        background: #4A90E2 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        width: 100%;
        height: 3.5em;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }

    /* Убираем лишние отступы у Streamlit */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Отрисовка всего интерфейса ВНУТРИ одной панели
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# Заголовок теперь внутри стекла
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Используем колонки, но на мобильных они встанут красиво друг под другом
uploaded_files = st.file_uploader(
    "Загрузить файл", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

st.write("") # Отступ

convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

st.markdown('</div>', unsafe_allow_html=True)

# ЛОГИКА
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Готово! Ваш файл собран.")
        st.download_button(
            label="📥 СКАЧАТЬ PDF",
            data=pdf_bytes,
            file_name="Finevych_PDF.pdf",
            mime="application/pdf"
        )
        
        # Предпросмотр (с матовым эффектом)
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="500" style="border-radius:15px; border: 1px solid rgba(255,255,255,0.2); margin-top:20px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Миниатюры загруженных фото
    st.write(f"🖼 Выбрано фото: {len(images)}")
    cols = st.columns(3)
    for i, img in enumerate(images):
        cols[i % 3].image(img, use_container_width=True)
