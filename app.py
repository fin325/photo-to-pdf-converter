import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы (ОБЯЗАТЕЛЬНО должна быть первой командой Streamlit)
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Финальный блок стилей
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    .stApp {
        background-color: #F5E6D3 !important;
    }

    .glass-container {
        background-color: #F5E6D3 !important;
        border: none !important;
        padding: 10px;
        margin-top: 10px;
        text-align: center;
    }

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
        padding: 10px !important;
    }
    
    /* Скрываем стандартную иконку и текст "Drag and drop" */
    div[data-testid="stFileUploader"] section > i, 
    div[data-testid="stFileUploader"] section > span {
        display: none !important;
    }

    /* === МАГИЯ ЗДЕСЬ: Замена текста про 200MB === */
    div[data-testid="stFileUploader"] section > small {
        font-size: 0px !important; /* Скрываем оригинальный текст */
    }
    
    div[data-testid="stFileUploader"] section > small::after {
        content: "Нажмите чтобы выбрать фото" !important;
        font-size: 16px !important;
        color: #1A3A5F !important;
        display: block !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* КНОПКА ЗАГРУЗИТЬ */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
        background-color: #1A3A5F !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* === Замена английского текста на кнопке 'Browse files' === */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] p {
        display: none !important; /* Скрываем "Browse files" */
    }
    
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]::after {
        content: "Выбрать файлы" !important; /* Наш новый текст кнопки */
        display: block !important;
        font-weight: 700 !important;
        font-family: 'Montserrat', sans-serif !important;
        color: white !important;
    }

    /* Настройка отображения списка файлов */
    div[data-testid="stFileUploaderFile"] {
        background-color: rgba(26, 58, 95, 0.1) !important;
        border-radius: 10px !important;
        padding: 5px !important;
        margin-top: 5px !important;
    }

    /* СТИЛИЗАЦИЯ КРЕСТИКА (КНОПКИ УДАЛЕНИЯ) */
    button[data-testid="stFileUploaderDeleteBtn"] {
        color: #800000 !important;
    }
    
    button[data-testid="stFileUploaderDeleteBtn"] svg {
        fill: #800000 !important;
        transform: scale(1.2);
    }

    /* КНОПКИ PDF */
    .stButton>button p, .stButton>button,
    .stDownloadButton>button p, .stDownloadButton>button {
        color: #F5E6D3 !important; 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }
    .stButton>button {
        background-color: #1A3A5F !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
    }
    .stDownloadButton>button {
        background-color: #2E5A88 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
    }

    hr { border-top: 1px solid #1A3A5F !important; }
    .block-container { padding-top: 2rem !important; }
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
            images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes = pdf_buffer.getvalue()
        
        st.success("PDF успешно создан!")
        st.download_button(label="📥 СКАЧАТЬ ВАШ PDF", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")
        
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600" style="border-radius:15px; border: 2px solid #1A3A5F; margin-top:20px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown("---")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
