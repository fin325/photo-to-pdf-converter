import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. ПОЛНЫЙ CSS (С переводом всех системных надписей)
st.markdown("""
    <style>
    /* Фон приложения */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        background-attachment: fixed;
    }

    .title-text {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* ЗОНА ЗАГРУЗКИ */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }

    /* --- ПЕРЕВОД ТЕКСТА "Drag and drop" --- */
    /* Скрываем старый текст */
    div[data-testid="stFileUploader"] section > div {
        display: none !important;
    }
    
    /* Вставляем новый русский текст сверху */
    div[data-testid="stFileUploader"] section::before {
        content: "Перетащите фото сюда";
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
        display: block;
    }

    /* Вставляем пояснение про лимит под низ */
    div[data-testid="stFileUploader"] section::after {
        content: "Лимит 200МБ на файл • JPG, JPEG, PNG";
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 13px;
        display: block;
        margin-top: 10px;
    }

    /* КНОПКА ЗАГРУЗКИ */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: transparent !important;
        font-size: 0 !important;
        border-radius: 10px !important;
        margin: 10px auto !important;
    }

    div[data-testid="stFileUploader"] button::after {
        content: "📥 Выбрать файлы";
        font-size: 16px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        visibility: visible !important;
    }

    /* ИМЕНА ФАЙЛОВ */
    div[data-testid="stFileUploaderFileName"] {
        color: #ffffff !important;
    }

    /* КРЕСТИКИ И ИКОНКИ */
    div[data-testid="stFileUploader"] svg {
        fill: white !important;
    }

    /* ГЛАВНАЯ КНОПКА "СОЗДАТЬ PDF" */
    .stButton>button {
        background: #3b82f6 !important;
        color: white !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.8em !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3) !important;
    }

    /* Тексты подсказок */
    .stMarkdown, p, span, label {
        color: #cbd5e1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ИНТЕРФЕЙС
st.markdown('<p class="title-text">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "uploader", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

# 4. ЛОГИКА
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    if convert_clicked:
        with st.spinner('Создаем PDF...'):
            pdf_buffer = io.BytesIO()
            images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes = pdf_buffer.getvalue()
        
        st.success("PDF готов!")
        st.download_button("📥 СКАЧАТЬ PDF", data=pdf_bytes, file_name="Finevych_PDF.pdf", mime="application/pdf")
        
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="500" style="border-radius:16px; border: none; background:white;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Предпросмотр фото
    st.markdown("---")
    cols = st.columns(3)
    for i, img in enumerate(images):
        cols[i % 3].image(img, use_container_width=True)
else:
    st.info("💡 Просто перетащите фотографии в рамку выше.")
