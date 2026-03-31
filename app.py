import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Блок стилей
st.markdown("""
    <style>
    /* Подключаем шрифт Montserrat специально для кнопок */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    /* Основной фон приложения (светло-кофейный) */
    .stApp {
        background-color: #F5E6D3 !important;
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
    }

    /* ЗОНА ЗАГРУЗКИ */
    div[data-testid="stFileUploader"] {
        background-color: #EADBC8 !important;
        border: 2px dashed #1A3A5F !important;
        border-radius: 15px !important;
    }
    
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

    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        font-size: 16px !important;
        color: #F5E6D3 !important; 
        font-weight: bold !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] ~ button::after,
    div[data-testid="stFileUploader"] [data-file-count] ~ button::after {
        content: "❌ Отменить всё" !important;
        color: #800000 !important; /* Текст "Отменить все" тоже сделаем бордовым */
    }

    /* ЦВЕТ ИМЕН ФАЙЛОВ И КРЕСТИКОВ УДАЛЕНИЯ */
    div[data-testid="stFileUploaderFileName"], 
    div[data-testid="stFileUploaderFileData"] {
        color: #1A3A5F !important;
    }

    /* Делаем иконку крестика (удаления) БОРДОВОЙ */
    div[data-testid="stFileUploader"] svg {
        fill: #800000 !important; /* ИЗМЕНЕНО: на темно-красный / бордовый */
    }

    /* КНОПКА "СОЗДАТЬ PDF" — КОФЕЙНЫЙ ТЕКСТ И ШРИФТ MONTSERRAT */
    .stButton>button p, .stButton>button div, .stButton>button {
        color: #F5E6D3 !important; 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }
    .stButton>button {
        background-color: #1A3A5F !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
    }

    /* КНОПКА "СКАЧАТЬ PDF" — КОФЕЙНЫЙ ТЕКСТ И ШРИФТ MONTSERRAT */
    .stDownloadButton>button p, .stDownloadButton>button div, .stDownloadButton>button {
        color: #F5E6D3 !important; 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }
    .stDownloadButton>button {
        background-color: #2E5A88 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
    }

    hr {
        border-top: 1px solid #1A3A5F !important;
    }

    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ИНТЕРФЕЙС
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
        
        st.download_button(
            label="📥 СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="Finevych_Document.pdf",
            mime="application/pdf"
        )
        
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe src="data:application/pdf;base64,{b64}" 
                    width="100%" height="600" 
                    style="border-radius:15px; border: 2px solid #1A3A5F; margin-top:20px;">
            </iframe>'''
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown("---")
    st.write("🖼 Исходные изображения:")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
