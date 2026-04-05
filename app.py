# 2. Финальный блок стилей
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

    /* ЗОНА ЗАГРУЗКИ */
    div[data-testid="stFileUploader"] {
        background-color: #EADBC8 !important;
        border: 2px dashed #1A3A5F !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    
    /* Скрываем стандартную иконку и текст "Drag and drop", но НЕ файлы */
    div[data-testid="stFileUploader"] section > i, 
    div[data-testid="stFileUploader"] section > span {
        display: none !important;
    }

    /* КНОПКА ЗАГРУЗИТЬ (делаем её красивой) */
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
        background-color: #1A3A5F !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    /* Настройка отображения списка файлов */
    div[data-testid="stFileUploaderFile"] {
        background-color: rgba(26, 58, 95, 0.1) !important;
        border-radius: 10px !important;
        padding: 5px !important;
        margin-top: 5px !important;
    }

    /* СТИЛИЗАЦИЯ КРЕСТИКА (КНОПКИ УДАЛЕНИЯ) */
    button[data-testid="stFileUploaderDeleteBtn"] {
        color: #800000 !important;
    }
    
    button[data-testid="stFileUploaderDeleteBtn"] svg {
        fill: #800000 !important;
        transform: scale(1.2);
    }

    /* КНОПКИ PDF */
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

    hr { border-top: 1px solid #1A3A5F !important; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)
