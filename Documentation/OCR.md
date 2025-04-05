# 🧾 OCR (Optical Character Recognition) with Python

This is a simple Python class that extracts text from images using the `pytesseract` library and `PIL` (Pillow). It wraps the basic functionality of Tesseract OCR into a reusable class.

---

## 📌 Overview

The `OCR` class allows you to:

- Load an image from a given path
- Extract text from the image using OCR (Optical Character Recognition)
- Return or print the extracted text

---

## 🛠️ Requirements

### 📦 Install Python Packages

```bash
pip install pytesseract Pillow


``` python 

if __name__ == "__main__":
    image_path = "/content/test.jpg"  # Update with your actual image path
    extractor = OCR(image_path)
    extracted_text = extractor.extract_text_from_image()
    ```