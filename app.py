import streamlit as st
from PIL import Image
import io
import base64

# ======================= GLASSMORPHISM СТИЛЬ =======================
def set_glassmorphism_style(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()

        glass_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .main .block-container {{
            background: rgba(255, 255, 255, 0.28);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.45);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 40px 35px;
            max-width: 1100px;
            margin: 30px auto;
        }}

        header {{ background: transparent !important; }}

        .title {{
            text-align: center;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #1e40af, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.45rem;
            color: #1e3a8a;
            margin-bottom: 45px;
            font-weight: 500;
        }}

        /* Стеклянный загрузчик */
        .stFileUploader > section {{
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            border: 2.5px dashed #60a5fa;
            border-radius: 20px;
            padding: 45px 25px;
        }}

        .stFileUploader label {{
            background: linear-gradient(135deg, #2563eb, #1e40af) !important;
            color: white !important;
            padding: 18px 45px !important;
            border-radius: 16px !important;
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
            width: 100% !important;
        }}

        .stFileUploader label:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.55) !important;
        }}

        /* Кнопка конвертации */
        .stButton > button {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            font-size: 1.3rem;
            font-weight: 700;
            padding: 18px 50px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.45);
            width: 100%;
            height: 62px;
        }}

        .stButton > button:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(37, 99, 235, 0.6);
        }}

        .stImage img {{
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        }}
        </style>
        """
        st.markdown(glass_css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"❌ Файл фона не найден: {image_path}")
        st.info("Убедись, что файл лежит по пути: img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg")

# ======================= ЗАПУСК СТИЛЯ =======================
set_glassmorphism_style("img/7c66a165-7bda-4830-843d-bf2839d5eb1e.jpeg")

# ======================= ПРИЛОЖЕНИЕ =======================
st.set_page_config(page_title="Foto to PDF", page_icon="📄", layout="centered")

st.markdown('<h1 class="title">Foto to PDF</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">von Finevych A.</p>', unsafe_allow_html=True)

# Загрузка файлов
uploaded_files = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# ======================= ОСНОВНАЯ ЛОГИКА =======================
if uploaded_files:
    st.success(f"✅ Загружено изображений: **{len(uploaded_files)}**")

    images = []
    num_cols = min(5, len(uploaded_files))
    cols = st.columns(num_cols)

    for idx, file in enumerate(uploaded_files):
        img = Image.open(file).convert("RGB")
        images.append(img)
        
        with cols[idx % num_cols]:
            st.image(img, use_column_width=True)

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

        col1, col2 = st.columns(2)
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
                    width="100%" height="780" 
                    style="border: none; border-radius: 12px;">
            </iframe>
        ''', unsafe_allow_html=True)