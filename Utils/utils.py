# read_files.py
import os
from collections import namedtuple
from Utils.ai_startup_utility import AIStartupUtility
import os
from docx import Document



def read_file(uploaded_file):
    """
    Reads a single uploaded file (pdf, docx, doc, txt) and extracts text content.
    For .doc and .docx, converts to PDF using LibreOffice and uses PDF extraction.
    :param uploaded_file: streamlit UploadedFile object
    :return: extracted text as string
    """
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    analyst = AIStartupUtility()

    if ext == ".pdf":
        try:
            analyst = AIStartupUtility()
            text_data = analyst.extract_text_from_pdf(filename)
            print(text_data)
            text =text_data
        except Exception as e:
            text = f"[Error reading PDF file: {e}]"

    elif ext==".docx":
        try:
            doc = Document(filename)
            text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
            return '\n'.join(text)
        except Exception as e:
            print(e)
            return text

    elif ext == ".txt":
        try:
            text = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            text = f"[Error reading text file: {e}]"
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


