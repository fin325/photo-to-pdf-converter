import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Кастомные стили для красоты (в стиле твоего HTML)
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 5px;
    }
    .author-line {
        text-align: center;
        font-size: 14px;
        opacity: 0.7;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #28a745;
        color: white;
        font-weight: bold;
    }
    /* Стиль для области загрузки */
    .stFileUploader {
        padding-top: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок в одну строку
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# 3. Блок управления (Кнопки в ряд сразу под заголовком)
col1, col2 = st.columns(2)

with col1:
    # Загрузчик файлов (скрываем стандартный текст для компактности)
    uploaded_files = st.file_uploader(
        "Выбрать фото",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    st.caption("⬅️ 1. Выберите изображения")

# Подготовка данных
images = []
pdf_bytes = None

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

with col2:
    # Кнопка конвертации
    convert_clicked = st.button("🚀 Конвертировать", disabled=not uploaded_files)
    st.caption("2. Создайте PDF ➡️")
    
    if convert_clicked and images:
        pdf_buffer = io.BytesIO()
        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )
        pdf_bytes = pdf_buffer.getvalue()
        st.success("Готово!")

# Разделитель
st.markdown("---")

# 4. Секция предпросмотра и скачивания
if uploaded_files:
    # Если PDF готов, показываем кнопку скачивания
    if pdf_bytes:
        st.download_button(
            label="📥 СКАЧАТЬ ГОТОВЫЙ PDF",
            data=pdf_bytes,
            file_name="converted_finevych.pdf",
            mime="application/pdf"
        )

    # Список загруженных картинок в виде сетки
    st.write(f"Загружено файлов: {len(uploaded_files)}")
    grid_cols = st.columns(4)
    for idx, img in enumerate(images):
        with grid_cols[idx % 4]:
            st.image(img, use_container_width=True)

    # Предпросмотр PDF (в самом низу)
    if pdf_bytes:
        st.markdown("### 📄 Просмотр:")
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{b64}" 
                width="100%" 
                height="600"
                type="application/pdf">
            </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("👋 Пожалуйста, выберите фото для начала работы.")
