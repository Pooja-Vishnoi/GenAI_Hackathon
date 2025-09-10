import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Constants
ELIGIBLE_SHIPPING_METHODS = ["INSURED"]
ELIGIBLE_REASONS = ["DAMAGED", "NEVER_ARRIVED"]


def get_purchase_history(purchaser: str) -> List[Dict[str, Any]]:
    
     return [{'aa':'bb'}]


def check_refund_eligibility(reason: str, shipping_method: str) -> bool:
   
    return True


def process_refund(amount: float, order_id: str) -> str:
    

    return f"✅ Refund {refund_id} successful! We will credit ${amount:.2f} to your account within 2 business days."

# ----------------------- without cloud vision -----------------------
# pip install PyPDF2
import PyPDF2
def pdf_to_text_pypdf2(pdf_path):
    text_content = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_content += page.extract_text() or ""
    return text_content

# if __name__ == "__main__":
#     pdf_path = "pitch_deck.pdf"
#     text = pdf_to_text_pypdf2(pdf_path)

# ---------------------------- with cloud vision -----------------------------
# Create a service account key and set it in terminal: 
# setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\service-account.json"
# pip install google-cloud-vision
from google.cloud import vision_v1 as vision
import io

def pdf_to_text_cloud_vision(pdf_path):
    client = vision.ImageAnnotatorClient()

    text_content = ""
    with io.open(pdf_path, "rb") as f:
        content = f.read()

    # Vision API expects images, so extract per page
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    text_content = response.full_text_annotation.text
    return text_content


# if __name__ == "__main__":
#     pdf_path = "pitch_deck.pdf"
#     text = pdf_to_text_cloud_vision(pdf_path)
#     print(text[:1000])

# ---------------------------------------------------------------------
# Autodetect
def pdf_to_text(pdf_path):
    """Auto-detect and extract text from PDF (digital or scanned)."""
    # Step 1: Try digital extraction
    text = extract_text_pypdf2(pdf_path)

    if text and len(text.split()) > 20:  # enough words found → likely digital
        print("✅ Extracted using PyPDF2 (digital PDF)")
        return text
    else:
        print("⚠️ Falling back to Google Cloud Vision OCR (scanned PDF)")
        return extract_text_cloud_vision(pdf_path)


