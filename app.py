import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. УЛУЧШЕННЫЙ CSS (Исправляем видимость имен файлов и кнопку отмены)
st.markdown("""
    <style>
    /* Глубокий темно-синий матовый фон */
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
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
    }

    /* ИМЕНА ФАЙЛОВ - Делаем БЕЛЫМИ и заметными */
    div[data-testid="stFileUploaderFileName"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* КНОПКА ЗАГРУЗКИ / ОТМЕНЫ */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: transparent !important;
        font-size: 0 !important;
        border-radius: 10px !important;
    }

    /* Если файлов НЕТ - пишем "Загрузить фото" */
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        font-size: 16px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        visibility: visible !important;
    }

    /* Если файлы ЕСТЬ - меняем текст на "Сбросить всё" (на селекторе с файлами) */
    div[data-testid="stFileUploader"] [data-file-count] ~ button::after {
        content: "❌ Отменить всё" !important;
    }

    /* ВОЗВРАЩАЕМ КРЕСТИК удаления одного файла */
    div[data-testid="stFileUploader"] svg {
        fill: white !important;
        display: block !important; /* Прошлый раз мы его скрыли, теперь возвращаем */
    }

    /* КНОПКА СОЗДАТЬ PDF */
    .stButton>button {
        background: #3b82f6 !important;
        color: white !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        margin-top: 10px !important;
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
    "upload", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

# 4. ЛОГИКА
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    # Конвертация
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Документ готов!")
        st.download_button("📥 СКАЧАТЬ PDF", data=pdf_bytes, file_name="Finevych_PDF.pdf", mime="application/pdf")
        
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="500" style="border-radius:16px; border: none; margin-top:20px; background:white;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Галерея превью
    st.markdown("---")
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            st.image(img, use_container_width=True)
else:
    st.info("💡 Нажмите кнопку выше, чтобы выбрать фото.")
