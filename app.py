import streamlit as st
from PIL import Image
import io
import base64

# ========================== ФОН СТРАНИЦЫ ==========================
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    
    page_bg_img = f'''
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Полупрозрачный слой для лучшей читаемости текста и виджетов */
    [data-testid="stAppViewContainer"] > div:first-child {{
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 15px;
        padding: 20px 15px;
        margin: 10px;
    }}

    /* Делаем заголовок и текст чуть более контрастными */
    h1, h2, h3, .stMarkdown {{
        color: #1e3a8a !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


# ======================= УСТАНОВКА ФОНА =======================
set_background("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg")

# ======================= ОСНОВНОЕ ПРИЛОЖЕНИЕ =======================
st.set_page_config(
    page_title="Image to PDF", 
    page_icon="📄",
    layout="centered"   # можно поменять на "wide", если хочешь шире
)

st.title("📄 Image → PDF Converter")

# Загрузка изображений
uploaded_files = st.file_uploader(
    "Загрузите изображения",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Загружено файлов: {len(uploaded_files)}")

    images = []

    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

        # Предпросмотр
        st.image(img, width=150)

    if st.button("🚀 Конвертировать в PDF"):
        pdf_buffer = io.BytesIO()

        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )

        pdf_bytes = pdf_buffer.getvalue()

        st.success("✅ PDF успешно создан!")

        # Кнопка скачивания
        st.download_button(
            label="📥 Скачать PDF",
            data=pdf_bytes,
            file_name="converted.pdf",
            mime="application/pdf"
        )

        # Просмотр PDF в браузере
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{b64}" 
                width="100%" 
                height="600"
                type="application/pdf">
            </iframe>
        '''

        st.markdown("### 👇 Просмотр PDF:")
        st.markdown(pdf_display, unsafe_allow_html=True)