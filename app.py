import streamlit as st
from PIL import Image
import io
import base64

# ======================= ФОН СТРАНИЦЫ =======================
def set_background(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Полупрозрачный слой для читаемости */
        .stApp > div {{
            background-color: rgba(255, 255, 255, 0.92);
            border-radius: 16px;
            padding: 25px 20px;
            margin: 15px auto;
            max-width: 96%;
        }}

        /* Прозрачный header */
        header {{
            background-color: rgba(0, 0, 0, 0) !important;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Файл фона не найден: {image_path}")

# ======================= УСТАНОВКА ФОНА =======================
set_background("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg")

# ======================= ОСНОВНОЕ ПРИЛОЖЕНИЕ =======================
st.set_page_config(
    page_title="Foto to PDF",
    page_icon="📄",
    layout="centered"
)

# ======================= КРАСИВАЯ НАДПИСЬ ВВЕРХУ =======================
st.markdown("""
    <h1 style='
        text-align: center; 
        color: #1e40af; 
        font-size: 2.8rem; 
        margin-bottom: 8px;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.9);
    '>
        Foto to PDF
    </h1>
    <p style='
        text-align: center; 
        color: #334155; 
        font-size: 1.25rem; 
        margin-top: -10px;
        margin-bottom: 30px;
        font-weight: 500;
    '>
        von Finevych A.
    </p>
""", unsafe_allow_html=True)

# ======================= КРАСИВАЯ КНОПКА ЗАГРУЗКИ =======================
st.markdown("""
    <style>
    div.stFileUploader > section {
        padding: 25px;
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.85);
    }
    
    /* Стилизация кнопки загрузки */
    .stFileUploader label {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: white !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-align: center !important;
        border: none !important;
    }
    
    .stFileUploader label:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
        background: linear-gradient(135deg, #1e40af, #1e3a8a) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Загрузка файлов (сразу под надписью)
uploaded_files = st.file_uploader(
    "Загрузите изображения (jpg, jpeg, png)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"   # скрываем стандартную подпись
)

# ======================= ОСНОВНАЯ ЛОГИКА =======================
if uploaded_files:
    st.success(f"Загружено файлов: **{len(uploaded_files)}**")

    images = []
    cols = st.columns(5)  # предпросмотр в несколько колонок

    for idx, file in enumerate(uploaded_files):
        img = Image.open(file).convert("RGB")
        images.append(img)
        
        with cols[idx % 5]:
            st.image(img, use_column_width=True)

    if st.button("🚀 Конвертировать в PDF", type="primary", use_container_width=True):
        pdf_buffer = io.BytesIO()

        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )

        pdf_bytes = pdf_buffer.getvalue()

        st.success("✅ PDF успешно создан!")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Скачать PDF",
                data=pdf_bytes,
                file_name="converted.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # Просмотр PDF
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{b64}" 
                width="100%" 
                height="700"
                type="application/pdf">
            </iframe>
        '''

        st.markdown("### 👇 Просмотр PDF в браузере:")
        st.markdown(pdf_display, unsafe_allow_html=True)