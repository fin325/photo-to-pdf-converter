# Foto zu PDF Converter

![Tests](https://github.com/fin325/photo-to-pdf-converter/actions/workflows/python-tests.yml/badge.svg)

Konvertiert JPG/PNG-Fotos in eine mehrseitige PDF-Datei. Läuft vollständig im Browser — keine Datenspeicherung auf dem Server.

-----

## 🚀 Live-Demo

🔗 [photo-to-pdf-converter-efhy6yri2rkf4g5wnhbwqm.streamlit.app](https://photo-to-pdf-converter-efhy6yri2rkf4g5wnhbwqm.streamlit.app)

-----

## ⚙️ Tech Stack

|Komponente      |Technologie              |
|----------------|-------------------------|
|Framework       |Python, Streamlit        |
|Bildverarbeitung|Pillow (PIL)             |
|PDF-Erstellung  |Pillow Image.save()      |
|Hosting         |Streamlit Community Cloud|
|Tests           |pytest                   |
|CI/CD           |GitHub Actions           |

-----

## 📋 Features

- **Mehrere Formate** — JPG, JPEG, PNG
- **Mehrere Fotos** — jedes Foto wird zu einer eigenen PDF-Seite
- **RGBA-Unterstützung** — Bilder mit Transparenz werden korrekt konvertiert
- **Keine Datenspeicherung** — Verarbeitung im RAM (BytesIO), kein Upload auf Server
- **PDF-Vorschau** — direktes Anzeigen im Browser nach Erstellung
- **Automatische Tests** — 6 pytest-Tests mit GitHub Actions CI

-----

## 🗂️ Projektstruktur

```
photo-to-pdf-converter/
├── app.py                    # Streamlit-Anwendung
├── test_converter.py         # pytest-Tests
├── requirements.txt          # Abhängigkeiten
└── .github/
    └── workflows/
        └── python-tests.yml  # CI/CD Pipeline
```

-----

## 🧪 Tests

```bash
pip install pillow pytest
pytest test_converter.py -v
```

**Testergebnisse:**

```
test_converter.py::test_single_image_produces_pdf        PASSED
test_converter.py::test_multiple_images_produce_pdf      PASSED
test_converter.py::test_pdf_larger_with_more_images      PASSED
test_converter.py::test_png_image_converts_to_pdf        PASSED
test_converter.py::test_rgba_image_converts_to_pdf       PASSED
test_converter.py::test_large_image_converts_to_pdf      PASSED

6 passed in 1.2s
```

**Testabdeckung:**

- Einzelnes Foto → gültige PDF
- Mehrere Fotos → eine mehrseitige PDF
- Mehr Fotos = größere Datei
- PNG-Format wird korrekt verarbeitet
- RGBA mit Transparenz wird korrekt konvertiert
- Großes Bild (2000×2000) wird verarbeitet

-----

## 🔧 Lokale Entwicklung

```bash
git clone https://github.com/fin325/photo-to-pdf-converter.git
cd photo-to-pdf-converter
pip install -r requirements.txt
streamlit run app.py
```

-----

## 👨‍💻 Autor

**Artem Finevych** — Hattingen, NRW

🔗 [digital-mobil-deutschland.vercel.app](https://digital-mobil-deutschland.vercel.app)
