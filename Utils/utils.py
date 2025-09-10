# read_files.py
import os
import docx
from Utils.pdf_file_reader import extract_pdf_file_content
from PyPDF2 import PdfReader


def read_file(uploaded_file):
    """
    Reads a single uploaded file (pdf, docx, txt) and extracts text content.
    :param uploaded_file: streamlit UploadedFile object
    :return: extracted text as string
    """
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    text = ""

    if ext == ".pdf":
        # pdf_reader_dict = extract_pdf_file_content(uploaded_file)
        # print(pdf_reader_dict)
        # text = " ".join(pdf_reader_dict.values())
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    elif ext in [".docx", ".doc"]:  # docx handled, doc may be partial
        try:
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            text = f"[Error reading Word file: {e}]"

    elif ext == ".txt":
        text = uploaded_file.read().decode("utf-8", errors="ignore")

    else:
        text = f"[Unsupported file type: {ext}]"

    return text


def read_files(uploaded_files):
    """
    Reads multiple uploaded files and returns a dict of filename -> text content.
    :param uploaded_files: list of UploadedFile objects
    :return: dict {filename: text}
    """
    results = {}
    for uploaded_file in uploaded_files:
        results[uploaded_file.name] = read_file(uploaded_file)
    return results
