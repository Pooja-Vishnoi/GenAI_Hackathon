# AI Startup Analyst

ai_startup_analyst.py is a Python script designed to analyze startup pitch decks and related documents. It extracts text, images, and tables from PDFs, structures startup data into JSON format, evaluates startups based on predefined criteria, calculates a weighted final score, and generates insights using the Gemini API.

## Features

PDF Processing: Extracts text, image-based text (via OCR), and tabular data from PDFs using PyMuPDF, pytesseract, and pdfplumber.
Data Structuring: Converts extracted data into structured JSON using the Gemini API.
Startup Evaluation: Scores startups across nine parameters (e.g., Sector, Team Quality, Market Size) with justifications.
Final Score Calculation: Computes a weighted overall score based on parameter scores and predefined weights.
Insight Generation: Identifies red flags, green flags, and provides recommendations.
Output Storage: Saves extracted data to Excel or CSV files.

## Installation

Prerequisites
Ensure you have Python 3.8+ installed. Install the required packages using:
pip install pymupdf pytesseract Pillow pandas pdfplumber PyPDF2 google-generativeai python-dotenv

Install Tesseract OCR for image text extraction:

Windows: Download and install from Tesseract OCR.
Linux: sudo apt-get install tesseract-ocr
MacOS: brew install tesseract

Environment Setup

Create a .env file in the project root with your Gemini API key:GEMINI_API_KEY=your_api_key_here


Ensure the prompts/ directory contains:
attribute_extraction_prompt.py
startup_scoring_prompt.py
insight_prompt.py



Usage

Prepare Input: Place your PDF pitch deck in a data/ directory (e.g., data/presentation_04_05.pdf).
Run the Script: Execute ai_startup_analyst.py to process the PDF, evaluate the startup, and generate insights.

from ai_startup_analyst import AIStartupAnalyst

analyst = AIStartupAnalyst()
pdf_path = "data/presentation_04_05.pdf"

# Extract text, images, and tables from PDF
text_data = analyst.extract_text_from_pdf(pdf_path)
print(text_data)

# Extract structured company information
structured_company_info = analyst.get_company_json_from_gemini(pitch_deck_content=str(text_data))
print(structured_company_info)

# Evaluate startup based on predefined criteria
startup_score = analyst.startup_evaluation(structured_company_info)
print(startup_score)

# Calculate weighted final score
overall_score = analyst.calculate_final_score(startup_score)
print(overall_score)

# Generate insights (red flags, green flags, recommendations)
insight_data = analyst.derive_insight(structured_company_info, startup_score, overall_score)
print(insight_data)

Example Output
The script generates:

Extracted Data: Saved as Excel (*.xlsx) or CSV (*_text.csv, *_images.csv, *_table_*.csv) files.
Company JSON: Structured startup details (e.g., company name, sector, traction).
Evaluation Scores: Scores for nine parameters with justifications.
Final Score: Weighted overall score, e.g.:{
    "weighted_scores": {
        "Sector": {"score": 9, "weight": 5, "weighted": 45},
        "Team_Quality": {"score": 9, "weight": 25, "weighted": 225},
        ...
    },
    "overall_score": 8.1
}


## Insights: Red flags, green flags, and recommendations.

Project Structure

project_root/

├── data/                                     # Directory for input PDF files
├── prompts/                                   # Directory for prompt files
│   ├── attribute_extraction_prompt.py
│   ├── startup_scoring_prompt.py
│   ├── insight_prompt.py
├── .env                                     # Environment file for API key
├── ai_startup_analyst.py                    # Main script
├── README.md                                # This file

Scoring Criteria
The calculate_final_score function evaluates startups based on nine parameters with the following weights:

Sector: 5%
Team Quality: 25%
Market Size: 20%
Traction: 15%
Financials: 10%
Product Uniqueness: 10%
Competitive Landscape: 5%
Business Model Clarity: 5%
Risk Factors: 5%

Each parameter is scored from 1 to 10, and the final score is a weighted average:overall_score = sum(score × weight) / total_weight.
Limitations

Requires a stable internet connection for Gemini API calls.
Image OCR accuracy depends on image quality and Tesseract performance.
Table extraction may fail for complex or non-standard table formats.
Fallback to PyPDF2 if PyMuPDF fails, but it lacks image and table extraction.
The report_generation function is not implemented.

Troubleshooting

Missing API Key: Ensure the .env file contains a valid GEMINI_API_KEY.
Tesseract Not Found: Verify Tesseract is installed and added to your system PATH.
PDF Processing Errors: Check if the PDF is corrupted or password-protected.
JSON Parsing Errors: Ensure the Gemini API response contains valid JSON.
