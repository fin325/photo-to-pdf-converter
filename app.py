import streamlit as st
from PIL import Image
import io
import base64

# Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# Кастомные стили для красоты
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Заголовок в одну строку
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# 2. Блок управления (Кнопки в ряд)
col1, col2 = st.columns(2)

with col1:
    # Кнопка загрузки (стилизованная под "Browse")
    uploaded_files = st.file_uploader(
        "Шаг 1: Выберите фото",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed" # Скрываем текст, чтобы было чище
    )
    st.caption("👈 Нажмите, чтобы выбрать фото")

# Логика обработки
images = []
pdf_bytes = None

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

with col2:
    # Кнопка конвертации (активна только если файлы загружены)
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
        st.success("Готово!")

---

# 3. Секция предпросмотра и скачивания
if uploaded_files:
    st.subheader("🖼 Предпросмотр и загрузка")
    
    # Если PDF уже создан, показываем кнопку скачивания во всю ширину
    if pdf_bytes:
        st.download_button(
            label="📥 СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="converted_finevych.pdf",
            mime="application/pdf"
        )

    # Список загруженных картинок в виде сетки
    cols = st.columns(4)
    for idx, img in enumerate(images):
        with cols[idx % 4]:
            st.image(img, use_container_width=True)

    # Предпросмотр PDF (если готов)
    if pdf_bytes:
        st.markdown("### 📄 Просмотр готового файла:")
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
    st.info("👋 Пожалуйста, загрузите хотя бы одно изображение, чтобы начать.")
