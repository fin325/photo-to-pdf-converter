import streamlit as st
from PIL import Image
import io
import base64

# ======================= ТВОЙ КРАСИВЫЙ HTML + CSS =======================
html_header = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
    }

    /* Фон из твоей картинки */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg") center/cover no-repeat;
        filter: blur(25px);
        z-index: -1;
        opacity: 0.85;
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.09) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 50px rgba(0,0,0,0.4);
        padding: 50px 40px;
        max-width: 700px;
        margin: 40px auto;
        color: white;
    }

    h1 {
        font-size: 2.8rem;
        margin-bottom: 10px;
        text-align: center;
    }

    .subtitle {
        font-size: 1.35rem;
        opacity: 0.85;
        text-align: center;
        margin-bottom: 35px;
    }

    /* Красивая кнопка загрузки */
    .stFileUploader > section {
        background: rgba(255,255,255,0.12) !important;
        border: 2px dashed rgba(255,255,255,0.5) !important;
        border-radius: 18px;
        padding: 40px 20px;
    }

    .stFileUploader label {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        padding: 16px 40px !important;
        border-radius: 14px !important;
        font-size: 1.2rem !important;
        font-weight: 600;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stFileUploader label:hover {
        background: rgba(255,255,255,0.35) !important;
        transform: translateY(-3px);
    }

    /* Тёмно-синяя кнопка конвертации */
    .stButton > button {
        background-color: #1e3a8a !important;
        color: white !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        padding: 16px !important;
        border-radius: 14px !important;
        width: 100% !important;
        margin-top: 20px;
    }

    .stButton > button:hover {
        background-color: #172554 !important;
    }
</style>

<div style="text-align: center; margin-bottom: 20px;">
    <h1>📄 Foto to PDF</h1>
    <p class="subtitle">von Finevych A.</p>
</div>
"""

# ======================= ПРИЛОЖЕНИЕ =======================
st.set_page_config(page_title="Foto to PDF", page_icon="📄", layout="centered")

# Вставляем твой красивый HTML + CSS
st.markdown(html_header, unsafe_allow_html=True)

# ======================= ЛОГИКА =======================
uploaded_files = st.file_uploader(
    "Загрузите изображения (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="visible"
)

if uploaded_files:
    st.success(f"✅ Загружено изображений: **{len(uploaded_files)}**")

    images = []
    cols = st.columns(min(5, len(uploaded_files)))

    for idx, file in enumerate(uploaded_files):
        img = Image.open(file).convert("RGB")
        images.append(img)
        with cols[idx % len(cols)]:
            st.image(img, use_column_width=True)

    if st.button("🚀 Конвертировать в PDF"):
        with st.spinner("Создаём PDF файл..."):
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
                    width="100%" height="780px" 
                    style="border: none; border-radius: 16px; background: white;">
            </iframe>
        ''', unsafe_allow_html=True)