import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

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

    div[data-testid="stFileUploader"] {
        background-color: #EADBC8 !important;
        border: 2px dashed #1A3A5F !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    div[data-testid="stFileUploaderFileName"],
    div[data-testid="stFileUploaderFileData"],
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] small {
        color: #1A3A5F !important;
    }

    div[data-testid="stFileUploader"] svg {
        fill: #1A3A5F !important;
    }

    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
        background-color: #1A3A5F !important;
        color: #F5E6D3 !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 8px 20px !important;
    }

    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #2E5A88 !important;
    }

    div[data-testid="stFileUploader"] button[aria-label="Remove file"] svg {
        fill: #800000 !important;
        transform: scale(1.4) !important;
    }

    .stButton>button {
        background-color: #1A3A5F !important;
        color: #F5E6D3 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
    }

    .stButton>button:hover {
        background-color: #2E5A88 !important;
    }

    .stDownloadButton>button {
        background-color: #2E5A88 !important;
        color: #F5E6D3 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
    }

    hr { border-top: 1px solid #1A3A5F !important; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Выберите фото JPG/PNG для конвертации",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

convert_clicked = st.button("Создать PDF", disabled=not uploaded_files)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]

    st.write(f"Выбрано фотографий: **{len(images)}**")

    if convert_clicked:
        with st.spinner("Обработка..."):
            pdf_buffer = io.BytesIO()
            images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes = pdf_buffer.getvalue()

        st.success("PDF успешно создан!")
        st.download_button(
            label="СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="result.pdf",
            mime="application/pdf"
        )

        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = (
            '<iframe src="data:application/pdf;base64,' + b64 + '" '
            'width="100%" height="600" '
            'style="border-radius:15px; border: 2px solid #1A3A5F; margin-top:20px;">'
            '</iframe>'
        )
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown("---")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
