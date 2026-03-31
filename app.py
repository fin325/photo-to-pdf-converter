import streamlit as st
from PIL import Image
import io
import base64

# ======================= СТИЛИ =======================
st.markdown("""
<style>
    .stApp {
        background-image: url("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 40px 30px;
        max-width: 800px;
        margin: 30px auto;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }

    /* Заголовок - белый матовый с тенью */
    .title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        font-size: 1.45rem;
        color: rgba(255, 255, 255, 0.95);
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 35px;
    }

    /* Кнопка "Конвертировать в PDF" - белая матовая */
    .stButton > button {
        background: rgba(255, 255, 255, 0.85) !important;
        color: #1e3a8a !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        padding: 14px 32px !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        border: none !important;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.95) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }

    /* Улучшение зоны загрузки */
    .stFileUploader > section {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px dashed rgba(255, 255, 255, 0.6) !important;
        border-radius: 16px;
        padding: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ======================= ПРИЛОЖЕНИЕ =======================
st.set_page_config(page_title="Foto to PDF", page_icon="📄", layout="centered")

st.markdown('<h1 class="title">Foto to PDF</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">von Finevych A.</p>', unsafe_allow_html=True)

# Загрузка файлов
uploaded_files = st.file_uploader(
    "Загрузите изображения (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="visible"
)

# ======================= ЛОГИКА =======================
if uploaded_files:
    st.success(f"✅ Загружено: **{len(uploaded_files)}** изображений")

    images = []
    cols = st.columns(min(5, len(uploaded_files)))

    for idx, file in enumerate(uploaded_files):
        img = Image.open(file).convert("RGB")
        images.append(img)
        with cols[idx % len(cols)]:
            st.image(img, use_column_width=True)

    # Кнопка "Конвертировать в PDF" рядом с зоной загрузки
    if st.button("🚀 Конвертировать в PDF"):
        with st.spinner("Создаём PDF..."):
            pdf_buffer = io.BytesIO()
            images[0].save(
                pdf_buffer,
                format="PDF",
                save_all=True,
                append_images=images[1:]
            )
            pdf_bytes = pdf_buffer.getvalue()

        st.success("🎉 PDF успешно создан!")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.download_button(
                label="📥 Скачать PDF",
                data=pdf_bytes,
                file_name="converted.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown("### 📄 Просмотр PDF:")
        st.markdown(f'''
            <iframe src="data:application/pdf;base64,{b64}" 
                    width="100%" height="750" 
                    style="border: none; border-radius: 12px; background:white;">
            </iframe>
        ''', unsafe_allow_html=True)