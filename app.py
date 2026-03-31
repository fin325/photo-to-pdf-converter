import streamlit as st
from PIL import Image
import io
import base64

# Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# ЭКСТРЕМАЛЬНЫЙ CSS для переделки стандартной панели
st.markdown("""
    <style>
    /* 1. Фон всего приложения */
    .stApp {
        background: linear-gradient(135deg, #102a43 0%, #243b55 100%);
    }

    /* 2. Заголовок */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    /* 3. Матовая панель управления */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* 4. ХАК ДЛЯ КНОПКИ BROWSE FILES */
    /* Скрываем стандартный текст внутри загрузчика */
    section[data-testid="stFileUploader"] section button span {
        display: none;
    }
    /* Пишем свой текст поверх */
    section[data-testid="stFileUploader"] section button::after {
        content: "📥 Выбрать файлы";
        color: white;
        font-weight: bold;
    }
    
    /* Стилизуем саму зону загрузки (сделаем её матовой) */
    section[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px;
        padding: 10px;
    }

    /* 5. Кнопка Конвертировать */
    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px;
        height: 3.8em;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: 0.3s;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.02);
    }

    /* Тексты подсказок */
    .stMarkdown, p, span {
        color: #d1d9e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Отрисовка интерфейса
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Оборачиваем кнопки в "стеклянный" контейнер
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Загрузить файл", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with col2:
    # Кнопка конвертации
    st.write("") # Небольшой отступ
    convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)

st.markdown('</div>', unsafe_allow_html=True)

# Логика обработки
if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.write(f"✅ Выбрано изображений: {len(images)}")
    
    if convert_clicked:
        pdf_buffer = io.BytesIO()
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = pdf_buffer.getvalue()
        
        st.success("Документ сформирован!")
        
        st.download_button(
            label="📥 СКАЧАТЬ PDF",
            data=pdf_bytes,
            file_name="result.pdf",
            mime="application/pdf"
        )
        
        # Предпросмотр
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600" style="border-radius:15px; margin-top:20px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Миниатюры (сетка)
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
else:
    st.info("💡 Нажмите на панель слева, чтобы выбрать фотографии для конвертации.")
