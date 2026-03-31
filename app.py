import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Улучшенные стили: Матовый темно-синий фон и стеклянные элементы
st.markdown("""
    <style>
    /* Основной фон приложения */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        background-attachment: fixed;
    }

    /* Заголовок */
    .main-title {
        font-size: 34px;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 5px;
    }

    /* Матовая панель для кнопок */
    .glass-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    /* Стилизация кнопок */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        font-weight: bold;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    /* Кнопка скачивания (зеленоватый матовый) */
    .stDownloadButton>button {
        width: 100%;
        border-radius: 12px;
        background: rgba(40, 167, 69, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px);
        font-weight: bold;
    }

    /* Текст описания */
    .stMarkdown p {
        color: #e0e0e0;
    }
    
    /* Скрытие стандартной надписи загрузчика */
    .st-emotion-cache-1ae8k9d {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7);'>Конвертируйте ваши изображения в PDF за пару кликов</p>", unsafe_allow_html=True)

# 3. Матовая панель управления
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Переименованная кнопка загрузки
    uploaded_files = st.file_uploader(
        "Загрузить файл", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="visible" 
    )

images = []
pdf_bytes = None

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

with col2:
    st.write("##") # Отступ для выравнивания с кнопкой загрузки
    convert_clicked = st.button("🚀 Конвертировать", disabled=not uploaded_files)
    
    if convert_clicked and images:
        pdf_buffer = io.BytesIO()
        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )
        pdf_bytes = pdf_buffer.getvalue()
        st.success("PDF готов!")

st.markdown('</div>', unsafe_allow_html=True)

# 4. Секция предпросмотра
if uploaded_files:
    st.markdown("### 🖼 Ваши изображения")
    
    if pdf_bytes:
        st.download_button(
            label="📥 СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="converted_by_finevych.pdf",
            mime="application/pdf"
        )

    # Галерея
    grid_cols = st.columns(4)
    for idx, img in enumerate(images):
        with grid_cols[idx % 4]:
            st.image(img, use_container_width=True)

    # Просмотр PDF
    if pdf_bytes:
        st.markdown("### 📄 Предпросмотр документа")
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{b64}" 
                width="100%" 
                height="600"
                style="border-radius: 15px; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.5);"
                type="application/pdf">
            </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("✨ Чтобы начать, нажмите «Browse files» выше и выберите фотографии.")
