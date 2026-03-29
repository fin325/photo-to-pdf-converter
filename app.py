import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="Image to PDF", page_icon="📄")

st.title("📄 Image → PDF Converter")

# 🔼 ЗАГРУЗКА СРАЗУ ВВЕРХУ
uploaded_files = st.file_uploader(
    "Загрузите изображения",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Загружено файлов: {len(uploaded_files)}")

    images = []

    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

        # 👁 предпросмотр
        st.image(img, width=150)

    if st.button("🚀 Конвертировать в PDF"):
        pdf_buffer = io.BytesIO()

        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )

        pdf_bytes = pdf_buffer.getvalue()

        st.success("PDF готов!")

        # 🔽 КНОПКА СКАЧИВАНИЯ
        st.download_button(
            label="📥 Скачать PDF",
            data=pdf_bytes,
            file_name="converted.pdf",
            mime="application/pdf"
        )

        # 🌐 ОТКРЫТИЕ В БРАУЗЕРЕ (ВАЖНО!)
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{b64}" 
                width="100%" 
                height="600"
                type="application/pdf">
            </iframe>
        '''

        st.markdown("### 👇 Просмотр PDF:")
        st.markdown(pdf_display, unsafe_allow_html=True)
