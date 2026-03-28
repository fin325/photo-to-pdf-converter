import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Image to PDF Converter", page_icon="📄")

st.title("📄 Image → PDF Converter")
st.write("Загрузи одно или несколько изображений и скачай PDF")

uploaded_files = st.file_uploader(
    "Выбери изображения",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    images = []

    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

    if st.button("Создать PDF"):
        pdf_buffer = io.BytesIO()

        images[0].save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=images[1:]
        )

        st.success("PDF готов!")

        st.download_button(
            label="Скачать PDF",
            data=pdf_buffer.getvalue(),
            file_name="converted.pdf",
            mime="application/pdf"
        )
