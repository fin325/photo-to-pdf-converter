import streamlit as st
from PIL import Image
import io
import base64

# 1. Базовая настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Полный блок стилей (Dark Glass Morphisim)
st.markdown("""
    <style>
    /* Фон всего приложения */
    .stApp {
        background: linear-gradient(135deg, #102a43 0%, #243b55 100%) !important;
    }

    /* Главный матовый контейнер */
    .glass-container {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin-top: 20px;
        text-align: center;
    }

    /* Заголовок внутри панели */
    .main-title {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 25px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* --- СТИЛИЗАЦИЯ ЗАГРУЗЧИКА --- */
    /* Убираем стандартный серый фон загрузчика */
    div[data-testid="stFileUploader"] {
        background-color: transparent !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    
    /* Скрываем лишние надписи "Drag and drop" и иконки */
    div[data-testid="stFileUploader"] section div {
        display: none !important;
    }
    div[data-testid="stFileUploader"] svg {
        display: none !important;
    }

    /* СТРАТЕГИЯ ПОЛНОЙ ЗАМЕНЫ ТЕКСТА КНОПКИ */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: transparent !important; /* Делаем Browse Files невидимым */
        font-size: 0 !important;       /* Сжимаем текст в ноль */
        height: 3.5em !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        cursor: pointer !important;
    }

    /* Вставляем наш чистый текст */
    div[data-testid="stFileUploader"] button::after {
        content: "📥 Загрузить фото";
        font-size: 16px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        visibility: visible !important;
    }

    /* Кнопка "Создать PDF" */
    .stButton>button {
        background: #4A90E2 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4) !important;
        transition: 0.3s !important;
        margin-top: 15px !important;
    }
    
    .stButton>button:hover {
        background: #357ABD !important;
        transform: translateY(-2px);
    }

    /* Тексты статусов и подписи */
    .stMarkdown, p, span, label {
        color: #e0e0e0 !important;
    }

    /* Убираем лишние отступы сверху страницы */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ОСНОВНОЙ ИНТЕРФЕЙС
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# Заголовок (теперь точно внутри матовой панели)
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Область загрузки
uploaded_files = st.file_uploader(
    "upload", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Кнопка конвертации
convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

st.markdown('</div>', unsafe_allow_html=True)

# 4. ЛОГИКА ПРИЛОЖЕНИЯ
if uploaded_files:
    # Собираем список изображений
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.write(f"✅ Выбрано фото: **{len(images)}**")
    
    # Если нажали кнопку "Создать"
    if convert_clicked:
        with st.spinner('Магия создания PDF...'):
            pdf_buffer = io.BytesIO()
            images[0].save(
                pdf_buffer, 
                format="PDF", 
                save_all=True, 
                append_images=images[1:]
            )
            pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Готово! Ваш файл собран.")
        
        # Кнопка скачивания
        st.download_button(
            label="📥 СКАЧАТЬ ВАШ PDF",
            data=pdf_bytes,
            file_name="Finevych_PDF.pdf",
            mime="application/pdf"
        )
        
        # Фрейм предпросмотра
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe src="data:application/pdf;base64,{b64}" 
                    width="100%" height="600" 
                    style="border-radius:15px; border: 1px solid rgba(255,255,255,0.2); margin-top:20px;">
            </iframe>'''
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Показываем миниатюры загруженных фото (сетка 4 колонки)
    st.markdown("---")
    st.write("🖼 Предпросмотр выбранных фото:")
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)

else:
    # Подсказка, если ничего не загружено
    st.info("👋 Чтобы начать, нажмите на кнопку «Загрузить фото» выше.")
