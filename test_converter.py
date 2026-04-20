"""
Tests für Foto-zu-PDF Converter
Ausführen: pytest test_converter.py -v
"""

import io
import pytest
from PIL import Image


# ------------------- HELPERS -------------------

def make_test_image(color="red", size=(100, 100)):
    """Создаёт тестовое изображение в памяти"""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


def images_to_pdf(image_files):
    """Логика конвертации из app.py"""
    images = [Image.open(f).convert("RGB") for f in image_files]
    pdf_buffer = io.BytesIO()
    images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
    return pdf_buffer.getvalue()


# ------------------- TESTS -------------------

def test_single_image_produces_pdf():
    """Одно фото → валидный PDF"""
    img = make_test_image("blue")
    result = images_to_pdf([img])
    assert result[:4] == b"%PDF"


def test_multiple_images_produce_pdf():
    """Несколько фото → один PDF"""
    images = [make_test_image(c) for c in ["red", "green", "blue"]]
    result = images_to_pdf(images)
    assert result[:4] == b"%PDF"


def test_pdf_larger_with_more_images():
    """PDF из 3 фото больше чем из 1"""
    one = images_to_pdf([make_test_image("red")])
    three = images_to_pdf([make_test_image(c) for c in ["red", "green", "blue"]])
    assert len(three) > len(one)


def test_png_image_converts_to_pdf():
    """PNG конвертируется без ошибок"""
    img = Image.new("RGB", (100, 100), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    result = images_to_pdf([buf])
    assert result[:4] == b"%PDF"


def test_rgba_image_converts_to_pdf():
    """RGBA изображение (прозрачность) конвертируется корректно"""
    img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    result = images_to_pdf([buf])
    assert result[:4] == b"%PDF"


def test_large_image_converts_to_pdf():
    """Большое изображение (2000x2000) конвертируется"""
    img = make_test_image("green", size=(2000, 2000))
    result = images_to_pdf([img])
    assert result[:4] == b"%PDF"
    assert len(result) > 0
