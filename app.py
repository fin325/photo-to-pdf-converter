    /* 1. Цвет для всех иконок (листочек и крестик) остается синим/бордовым */
    div[data-testid="stFileUploader"] svg {
        fill: #1A3A5F !important; /* Листочек пусть будет синим, как текст */
    }

    /* 2. УВЕЛИЧИВАЕМ ТОЛЬКО КРЕСТИК */
    /* Мы ищем кнопку удаления по её атрибуту и увеличиваем только её иконку */
    div[data-testid="stFileUploader"] button[aria-label="Remove file"] svg, 
    div[data-testid="stFileUploader"] button[data-testid="stFileUploaderDeleteBtn"] svg {
        fill: #800000 !important;        /* Цвет только для крестика — бордовый */
        transform: scale(1.8) !important; /* Увеличиваем только крестик */
        transition: transform 0.2s ease !important;
    }

    /* Эффект при наведении только на крестик */
    div[data-testid="stFileUploader"] button[aria-label="Remove file"]:hover svg {
        transform: scale(2.2) !important; /* Еще больше при наведении */
    }
