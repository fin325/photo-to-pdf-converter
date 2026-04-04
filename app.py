import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import os

# 1. Настройка страницы
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Скрываем стандартные отступы Streamlit (подтягиваем всё вверх)
st.markdown("""
    <style>
    /* Убираем верхнюю панель и отступы контейнера */
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
    }
    #root > div:nth-child(1) > div > div > div > div > section > div {
        padding-top: 0px !important;
    }
    /* Делаем основной фон Streamlit темным под стать вашему HTML */
    .stApp {
        background-color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Логика поиска и загрузки вашего HTML
def render_custom_html():
    # Собираем путь к файлу: текущая папка -> website -> index.html
    html_path = os.path.join(os.path.dirname(__file__), "website", "index.html")
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Выводим ваш дизайн. Высоту (height) подстройте под размер вашей карточки
        components.html(html_content, height=520, scrolling=False)
    else:
        st.error(f"Ошибка: Не найден файл по пути {html_path}")

# Вызываем отрисовку дизайна
render_custom_html()

# 4. ФУНКЦИОНАЛ КОНВЕРТЕРА
st.markdown("<h3 style='color: white; text-align: center;'>Загрузите фото ниже</h3>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Выбор файлов", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    # Конвертация
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"📸 Выбрано изображений: {len(images)}")
    
    if st.button("🚀 СОЗДАТЬ PDF", use_container_width=True):
        with st.spinner('Склеиваем страницы...'):
            pdf_out = io.BytesIO()
            images[0].save(pdf_out, format="PDF", save_all=True, append_images=images[1:])
            
            st.success("PDF готов!")
            st.download_button(
                label="📥 СКАЧАТЬ РЕЗУЛЬТАТ",
                data=pdf_out.getvalue(),
                file_name="my_photos.pdf",
                mime="application/pdf",
                use_container_width=True
            )
