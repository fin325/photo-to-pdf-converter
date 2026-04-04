import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import os

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📄", layout="centered")

# 2. ГЛОБАЛЬНЫЙ CSS ДИЗАЙН (Меняем стандартный интерфейс Streamlit)
st.markdown("""
    <style>
    /* 1. Темный фон всего приложения и скрытие системной шапки */
    .stApp { background-color: #0f172a !important; }
    header { visibility: hidden !important; height: 0px !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 2rem !important; }
    #root > div:nth-child(1) > div > div > div > div > section > div { padding-top: 0px !important; }

    /* 2. ПОЛНАЯ ПЕРЕДЕЛКА СТАНДАРТНОГО ЗАГРУЗЧИКА ФАЙЛОВ */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border: 2px dashed rgba(255, 255, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 25px 15px !important;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #ffffff !important;
        box-shadow: 0 15px 40px rgba(37, 99, 235, 0.4) !important;
    }

    /* Прячем скучный стандартный текст Streamlit */
    div[data-testid="stFileUploader"] section > div > span,
    div[data-testid="stFileUploader"] section > div > small {
        display: none !important;
    }

    /* Добавляем свою красивую надпись внутрь загрузчика */
    div[data-testid="stFileUploader"] section > div::before {
        content: "☁️ Нажмите или перетащите фото сюда";
        color: white;
        font-size: 16px;
        font-weight: 600;
        display: block;
        text-align: center;
        margin-bottom: 12px;
    }

    /* Стилизуем кнопку "Browse files" внутри загрузчика */
    div[data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        width: 100% !important;
        font-size: 14px !important;
        font-weight: bold !important;
        transition: background-color 0.3s !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Цвет текста загруженных файлов */
    div[data-testid="stFileUploaderFileName"] { color: #ffffff !important; font-weight: bold !important;}
    div[data-testid="stFileUploaderFileData"] { color: rgba(255,255,255,0.7) !important; }

    /* 3. СТИЛИЗАЦИЯ ГЛАВНЫХ КНОПОК */
    /* Кнопка "Создать PDF" */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Кнопка "Скачать PDF" */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3) !important;
        margin-top: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ПОДГРУЖАЕМ ВАШУ КРАСИВУЮ HTML-ШАПКУ
def render_header():
    html_path = os.path.join(os.path.dirname(__file__), "website", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Высота всего 80px, так как там только заголовок!
        components.html(html_content, height=80, scrolling=False)
    else:
        st.markdown("<h2 style='color:white; text-align:center;'>Foto to PDF</h2>", unsafe_allow_html=True)

render_header()

# 4. ФУНКЦИОНАЛ ПРИЛОЖЕНИЯ (С уже примененным новым CSS)
uploaded_files = st.file_uploader(
    "Загрузка", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed" # Скрываем стандартный лейбл
)

if uploaded_files:
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.markdown(f"<p style='color: #60a5fa; font-weight: bold; text-align: center; margin-top: -10px;'>✅ Готово к обработке: {len(images)} шт.</p>", unsafe_allow_html=True)
    
    if st.button("🚀 СОЗДАТЬ PDF", use_container_width=True):
        with st.spinner('Конвертация...'):
            pdf_out = io.BytesIO()
            images[0].save(pdf_out, format="PDF", save_all=True, append_images=images[1:])
            
            st.success("Документ успешно создан!")
            st.download_button(
                label="📥 СКАЧАТЬ ВАШ PDF",
                data=pdf_out.getvalue(),
                file_name="converted_images.pdf",
                mime="application/pdf",
                use_container_width=True
            )
