import pdfplumber

def extract_text(pdf_file):
    """ 提取 PDF 文字，返回字符串 """
    text=""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
