import fitz
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)

def extract_pdf_text(path:str)->str:
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def extract_image_text(path:str)->str:
    res = ocr.ocr(path,cls=True)
    text=""
    for line in res:
        for word in line:
            text += word[1][0]+" "
    return text