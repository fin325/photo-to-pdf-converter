# 3. ИНТЕРФЕЙС
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">Foto to PDF von Finevych A.</p>', unsafe_allow_html=True)

# Создаем две колонки: одна для кнопки (60%), другая для описания (40%)
col_left, col_right = st.columns([3, 2])

with col_left:
    uploaded_files = st.file_uploader(
        "upload", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with col_right:
    # Добавляем отступ сверху, чтобы текст был на одном уровне с кнопкой
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: left; font-size: 14px; line-height: 1.4;'>
            <strong>ℹ️ Инструкция:</strong><br>
            • Выберите одно или несколько фото<br>
            • Форматы: JPG, PNG<br>
            • Затем нажмите «Создать PDF»
        </div>
    """, unsafe_allow_html=True)

# Кнопка конвертации (на всю ширину под колонками)
convert_clicked = st.button("🚀 Создать PDF", disabled=not uploaded_files)
st.markdown('</div>', unsafe_allow_html=True)
