import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Блок стилей: Светло-кофейный фон и Темно-синий текст
st.markdown("""
    <style>
    /* Основной фон приложения (светло-кофейный) */
    .stApp {
        background-color: #F5E6D3 !important;
        background-image: none !important;
    }

    /* Контейнер для интерфейса */
    .glass-container {
        background-color: #F5E6D3 !important;
        border: none !important;
        padding: 10px;
        margin-top: 10px;
        text-align: center;
    }

    /* Все заголовки и тексты (темно-синий) */
    h1, h2, h3, p, span, label, .main-title {
        color: #1A3A5F !important;
    }

    .main-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 25px;
        text-align: center;
    }

    /* ЗОНА ЗАГРУЗКИ */
    div[data-testid="stFileUploader"] {
        background-color: #EADBC8 !important; /* Чуть более темный кофейный для выделения зоны */
        border: 2px dashed #1A3A5F !important;
        border-radius: 15px !important;
    }
    
    /* Скрываем стандартный текст "Drag and Drop" */
    div[data-testid="stFileUploader"] section div {
        display: none !important;
    }

    /* КНОПКА ВНУТРИ ЗАГРУЗЧИКА */
    div[data-testid="stFileUploader"] button {
        background-color: #1A3A5F !important;
        color: transparent !important;
        font-size: 0 !important;
        height: 3.5em !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border: none !important;
    }

    /* Текст кнопки "Загрузить" */
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        font-size: 16px !important;
        color: #F5E6D3 !important; /* Кофейный текст на синей кнопке */
        font-weight: bold !important;
    }

    /* Текст кнопки при загрузке файлов */
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] ~ button::after,
    div[data-testid="stFileUploader"] [data-file-count] ~ button::after {
        content: "❌ Отменить всё" !important;
        color: #FF6B6B !important;
    }

    /* Названия загруженных файлов и их размер */
    div[data-testid="stFileUploaderFileName"], 
    div[data-testid="stFileUploaderFileData"] {
        color: #1A3A5F !important;
    }

    /* Кнопка "Создать PDF" */
    .stButton>button {
        background-color: #1A3A5F !important;
        color: #F5E6D3 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #12263F !important;
        box-shadow: 0 4px 10px rgba(26, 58, 95, 0.3) !important;
    }

    /* Кнопка "Скачать PDF" */
    .stDownloadButton>button {
        background-color: #2E5A88 !important;
        color: #F5E6D3 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        margin-top: 15px !important;
    }

    /* Горизонтальная линия */
    hr {
        border-top: 1px solid #1A3A5F !important;
    }

    /* Компактность страницы */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ИНТЕРФЕЙС
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# ЗАГРУЗКА
uploaded_files = st.file_uploader(
    "upload", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# КНОПКА КОНВЕРТАЦИИ
convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)
st.markdown('</div>', unsafe_allow_html=True)

# 4. ЛОГИКА
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.write(f"✅ Выбрано фотографий: **{len(images)}**")
    
    if convert_clicked:
        with st.spinner('Обработка...'):
            pdf_buffer = io.BytesIO()
            images[0].save(
                pdf_buffer, 
                format="PDF", 
                save_all=True, 
                append_images=images[1:]
            )
            pdf_bytes = pdf_buffer.getvalue()
        
        st.success("PDF успешно создан!")
        
        # СКАЧИВАНИЕ
        st.download_button(
            label="📥 СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="Finevych_Document.pdf",
            mime="application/pdf"
        )
        
        # ПРЕДПРОСМОТР PDF
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe src="data:application/pdf;base64,{b64}" 
                    width="100%" height="600" 
                    style="border-radius:15px; border: 2px solid #1A3A5F; margin-top:20px;">
            </iframe>'''
        st.markdown(pdf_display, unsafe_allow_html=True)

    # ПРЕДПРОСМОТР ФОТО (внизу)
    st.markdown("---")
    st.write("🖼 Исходные изображения:")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
