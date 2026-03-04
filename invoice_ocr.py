
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def extract_text_from_pdf(pdf_path):

    pages = convert_from_path(
        pdf_path,
        300,
        poppler_path=r"C:/Program Files/poppler-25.12.0/Library/bin"
    )

    full_text = ""

    for page in pages:
        open_cv_image = np.array(page)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
        open_cv_image = cv2.threshold(open_cv_image, 150, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(open_cv_image)
        full_text += text

    return full_text