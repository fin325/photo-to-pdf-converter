import streamlit as st
from PIL import Image
import io
import base64

# 1. Seiteneinstellungen / Настройка страницы / Page configuration
st.set_page_config(page_title="Foto to PDF", page_icon="📸", layout="centered")

# 2. Stilblock / Блок стилей / Style block
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');

    /* === OBEREN ABSTAND DER SEITE ENTFERNEN / УБИРАЕМ ЛИШНЕЕ ПРОСТРАНСТВО СВЕРХУ / REMOVE TOP PAGE PADDING === */
    .block-container { 
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
    }

    .stApp {
        background-color: #F5E6D3 !important;
    }

    .glass-container {
        background-color: #F5E6D3 !important;
        border: none !important;
        padding: 0px 10px 10px 10px !important; 
        margin-top: 0px !important;
        text-align: center;
    }

    h1, h2, h3, p, span, label {
        color: #1A3A5F !important;
    }

    /* === TITELSTIL / СТИЛЬ ЗАГОЛОВКА / TITLE STYLE === */
    .main-title {
        color: #1A3A5F !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        text-align: center !important;
        letter-spacing: 0.5px !important; 
        text-shadow: 2px 2px 5px rgba(26, 58, 95, 0.4) !important; 
        margin-top: 0px !important;
        margin-bottom: 20px !important; 
        white-space: nowrap !important;
    }

    /* UPLOAD-BEREICH / ЗОНА ЗАГРУЗКИ / UPLOAD AREA */
    div[data-testid="stFileUploader"] {
        background-color: #EADBC8 !important;
        border: 2px dashed #1A3A5F !important;
        border-radius: 15px !important;
        padding: 5px !important; 
    }
    
    /* Standardabstände im Upload-Bereich entfernen / Убираем стандартные отступы внутри зоны / Remove default padding inside upload area */
    div[data-testid="stFileUploader"] section {
        padding: 15px 10px !important; 
    }

    /* Nur Icons und "Drag and drop" Text ausblenden / Скрываем иконки и текст "Drag and drop" / Hide icons and "Drag and drop" text */
    div[data-testid="stFileUploader"] section > svg,
    div[data-testid="stFileUploader"] section > i, 
    div[data-testid="stFileUploader"] section > span {
        display: none !important;
    }

    /* "200MB per file" Hinweis einfärben / Подкрашиваем надпись "200MB per file" / Color the "200MB per file" hint */
    div[data-testid="stFileUploader"] small {
        color: #1A3A5F !important;
        font-family: 'Montserrat', sans-serif !important;
        opacity: 0.8 !important;
    }

    /* === EIGENER UPLOAD-TEXT / НАШ КОРОТКИЙ ТЕКСТ / CUSTOM UPLOAD TEXT === */
    div[data-testid="stFileUploader"] section::before {
        content: "📸 Foto auswählen";
        display: block !important;
        text-align: center !important;
        color: #1A3A5F !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important; 
        white-space: nowrap !important;
    }

    /* UPLOAD-SCHALTFLÄCHE (innerhalb des Bereichs) / КНОПКА ЗАГРУЗИТЬ (внутри окна) / UPLOAD BUTTON (inside area) */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
        background-color: #1A3A5F !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 10px !important;
        padding: 8px !important; 
    }
    
    /* Englischen Buttontext ausblenden / Замена английского текста на кнопке / Hide default English button text */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] p {
        display: none !important;
    }
    
    /* Deutschen Buttontext einblenden / Показываем немецкий текст кнопки / Show German button text */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]::after {
        content: "Dateien auswählen" !important;
        display: block !important;
        font-weight: 700 !important;
        font-family: 'Montserrat', sans-serif !important;
        color: white !important;
    }

    /* Darstellung der hochgeladenen Dateiliste / Настройка отображения списка файлов / Uploaded file list display */
    div[data-testid="stFileUploaderFile"] {
        background-color: rgba(26, 58, 95, 0.1) !important;
        border-radius: 10px !important;
        padding: 5px !important;
        margin-top: 5px !important;
    }

    /* LÖSCH-SCHALTFLÄCHE STILISIERUNG / СТИЛИЗАЦИЯ КРЕСТИКА (КНОПКИ УДАЛЕНИЯ) / DELETE BUTTON STYLING */
    button[data-testid="stFileUploaderDeleteBtn"] {
        color: #800000 !important;
    }
    
    button[data-testid="stFileUploaderDeleteBtn"] svg {
        fill: #800000 !important;
        transform: scale(1.2);
    }

    /* PDF-SCHALTFLÄCHEN / КНОПКИ PDF / PDF BUTTONS */
    .stButton>button p, .stButton>button,
    .stDownloadButton>button p, .stDownloadButton>button {
        color: #F5E6D3 !important; 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }
    .stButton>button {
        background-color: #1A3A5F !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
    }
    .stDownloadButton>button {
        background-color: #2E5A88 !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 3.5em !important;
    }

    hr { border-top: 1px solid #1A3A5F !important; margin: 1em 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BENUTZEROBERFLÄCHE / ИНТЕРФЕЙС / USER INTERFACE
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">Foto zu PDF von Finevych A.</p>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "upload", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

convert_clicked = st.button("🚀 PDF erstellen", disabled=not uploaded_files)
st.markdown('</div>', unsafe_allow_html=True)

# 4. PROGRAMMLOGIK / ЛОГИКА / PROGRAM LOGIC
if uploaded_files:
    # Bilder öffnen und in RGB konvertieren / Открываем изображения и конвертируем в RGB / Open images and convert to RGB
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
    
    st.write(f"✅ Fotos ausgewählt: **{len(images)}**")
    
    if convert_clicked:
        # PDF erstellen / Создаём PDF / Create PDF
        with st.spinner('Verarbeitung...'):
            pdf_buffer = io.BytesIO()
            images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes = pdf_buffer.getvalue()
        
        st.success("PDF erfolgreich erstellt!")
        # Download-Schaltfläche anzeigen / Показываем кнопку скачивания / Show download button
        st.download_button(label="📥 DEIN PDF HERUNTERLADEN", data=pdf_bytes, file_name="result.pdf", mime="application/pdf")
        
        # PDF-Vorschau im Browser / Предпросмотр PDF в браузере / PDF preview in browser
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600" style="border-radius:15px; border: 2px solid #1A3A5F; margin-top:20px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown("---")
    # Vorschau der hochgeladenen Fotos in 4 Spalten / Предпросмотр фото в 4 колонки / Preview uploaded photos in 4 columns
    cols = st.columns(4)
    for i, img in enumerate(images):
        cols[i % 4].image(img, use_container_width=True)
