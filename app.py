import streamlit as st
from PIL import Image
import io
import base64

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. ФИНАЛЬНЫЙ ДИЗАЙН: Темно-синий матовый фон
st.markdown("""
    <style>
    /* Глубокий темно-синий матовый фон на все приложение */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        background-attachment: fixed;
    }

    /* Убираем стандартные белые блоки Streamlit */
    .block-container {
        padding-top: 3rem !important;
        background-color: transparent !important;
    }

    /* Контейнер для кнопок - теперь он прозрачный и сливается с фоном */
    .main-panel {
        background: transparent !important;
        border: none !important;
        text-align: center;
        padding: 0px;
    }

    /* Титульное название сверху */
    .title-text {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 25px;
        text-align: center;
        letter-spacing: 0.5px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* СТИЛИЗАЦИЯ ЗАГРУЗЧИКА (Прозрачно-матовый) */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 15px !important;
        transition: 0.3s;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #4A90E2 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* СКРЫВАЕМ СТАНДАРТНЫЙ ТЕКСТ И ЗАМЕНЯЕМ НА НАШ */
    div[data-testid="stFileUploader"] section div {
        display: none !important;
    }
    div[data-testid="stFileUploader"] svg {
        display: none !important;
    }
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: transparent !important;
        font-size: 0 !important;
        height: 3.5em !important;
        width: 100% !important;
        border-radius: 12px !important;
    }
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        font-size: 16px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        visibility: visible !important;
    }

    /* КНОПКА СОЗДАТЬ PDF */
    .stButton>button {
        background: #3b82f6 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3) !important;
        margin-top: 10px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background: #2563eb !important;
        transform: translateY(-2px);
        box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4) !important;
    }

    /* Тексты сообщений */
    .stMarkdown, p, span, label {
        color: #94a3b8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ИНТЕРФЕЙС
st.markdown('<p class="title-text">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Кнопки загрузки и обработки
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
    
    st.write(f"📸 Фотографий в очереди: **{len(images)}**")
    
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("PDF документ готов!")
        
        st.download_button(
            label="📥 СКАЧАТЬ ГОТОВЫЙ ФАЙЛ",
            data=pdf_bytes,
            file_name="Finevych_PDF.pdf",
            mime="application/pdf"
        )
        
        # Предпросмотр (матовый фрейм)
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe src="data:application/pdf;base64,{b64}" 
                    width="100%" height="600" 
                    style="border-radius:16px; border: 1px solid rgba(255,255,255,0.1); margin-top:20px; background: white;">
            </iframe>'''
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Галерея превью (сетка)
    st.markdown("---")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)

else:
    st.info("💡 Нажмите «Загрузить фото», чтобы начать конвертацию.")
