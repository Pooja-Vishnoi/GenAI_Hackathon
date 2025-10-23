import logging
logger = logging.getLogger()

import fitz  
import pytesseract  
from PIL import Image
import io
import pandas as pd
import os
import pdfplumber
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
from agents.attribute_extraction_prompt import ATTRIBUTE_EXTRACTION_PROMPT
from agents.startup_scoring_prompt import STARTUP_SCORING_PROMPT
from agents.insight_prompt import INSIGHT_PROMPT
import json
from docx import Document

load_dotenv(dotenv_path="agents/.env")

# Initialize Gemini client
key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

class AIStartupUtility:

    def __init__(self):
        pass


    def extract_text_from_pdf(self, pdf_path):
        """Extract text, image text, and tables from a PDF file, store in Excel, and return data as a list of dictionaries"""
        PDFPLUMBER_AVAILABLE = True  
        OPENPYXL_AVAILABLE = True    
        PYPDF2_AVAILABLE = True  
        result = []
        text_data = []
        image_data = []
        table_data = []

        logger.info(f"Extracting text from PDF: {pdf_path}")
        
        try:
            # Open the PDF file using PyMuPDF
            logger.info("Opening PDF with PyMuPDF")
            logger.info(f"Pdf path: {pdf_path}")
            doc = fitz.open(pdf_path)
            logger.info(f"Number of pages in PDF: {len(doc)}")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_key = f"Page {page_num + 1}"
                page_dict = {
                    "page_no": page_num + 1,
                    "extracted_text": "Not available",
                    "extracted_text_from_image": "Not available",
                    "extracted_tabular_data": "Not available"
                }
                
                # Extract text from the page
                blocks = page.get_text("blocks")
                logger.info(f"Extracting text from page {page_num + 1}")
                page_text = "\n".join([block[4].strip() for block in blocks if block[6] == 0])  # Text only, skip images
                logger.info(f"Length of text extracted: {len(page_text)}")
                if page_text.strip():
                    page_dict["extracted_text"] = page_text
                    text_data.append({"Page": page_key, "Text": page_text})
                
                # If no text is extracted, take a page screenshot and perform OCR
                if not page_text.strip():
                    try:
                        # Render page to an image
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase resolution
                        temp_image_path = f"temp_page_{page_num + 1}.png"
                        pix.save(temp_image_path)
                        
                        # Perform OCR on the page image
                        img_pil = Image.open(temp_image_path)
                        ocr_text = pytesseract.image_to_string(img_pil).strip()
                        
                        # Delete the temporary image file
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                        
                        if ocr_text and len(ocr_text) > 10:  # Only meaningful text
                            page_dict["extracted_text_from_image"] = ocr_text
                            image_data.append({
                                "Page": page_key,
                                "Image": f"Page_Screenshot_{page_num + 1}",
                                "Text": ocr_text
                            })
                            logger.info(f"Extracted text from page screenshot on page {page_num + 1}")
                    except Exception as e:
                        logger.error(f"Error processing page screenshot on page {page_num + 1}: {str(e)}")
                
                # Extract text from images using OCR
                images = page.get_images(full=True)
                if images:
                    image_texts = []
                    for img_index, img in enumerate(images):
                        try:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            img_pil = Image.open(io.BytesIO(image_bytes))
                            
                            # Perform OCR on the image
                            ocr_text = pytesseract.image_to_string(img_pil).strip()
                            if ocr_text and len(ocr_text) > 10:  # Only meaningful text
                                image_texts.append(ocr_text)
                                image_data.append({
                                    "Page": page_key,
                                    "Image": f"Image {img_index + 1}",
                                    "Text": ocr_text
                                })
                        except Exception as e:
                            logger.error(f"Error processing image {img_index + 1} on page {page_num + 1}: {str(e)}")
                    if image_texts:
                        logger.info(f"Extracting text from images on page {page_num + 1}")
                        page_dict["extracted_text_from_image"] = "\n".join(image_texts)
                
                # Append page dictionary to result
                result.append(page_dict)
            
            # Close the PDF document
            doc.close()
            
            # Extract table content using pdfplumber, if available
            if PDFPLUMBER_AVAILABLE:
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        for page_num, page in enumerate(pdf.pages):
                            page_key = f"Page {page_num + 1}"
                            tables = page.extract_tables()
                            if tables:
                                table_texts = []
                                for table_index, table in enumerate(tables):
                                    # Filter out empty rows
                                    table = [row for row in table if any(cell for cell in row)]
                                    if table:
                                        # Use first row as headers or generate generic ones
                                        headers = table[0] if table and table[0] else [f"Column_{i + 1}" for i in range(len(table[1]))]
                                        headers = [str(h) if h is not None else f"Column_{i + 1}" for i, h in enumerate(headers)]
                                        # Create DataFrame for the table
                                        table_df = pd.DataFrame(table[1:], columns=headers)
                                        table_data.append({
                                            "Page": page_key,
                                            "Table": f"Table {table_index + 1}",
                                            "DataFrame": table_df
                                        })
                                        # Convert table to string for extracted_tabular_data
                                        table_text = "\n".join(["\t".join([str(cell) if cell is not None else "" for cell in row]) for row in table])
                                        table_texts.append(table_text)
                                if table_texts:
                                    result[page_num]["extracted_tabular_data"] = "\n".join(table_texts)
                except Exception as e:
                    logger.error(f"Error extracting tables with pdfplumber: {str(e)}. Skipping table extraction.")
            else:
                logger.warning("Table extraction skipped: pdfplumber not installed.")
            
            # Save data to file (Excel if openpyxl available, else CSV)
            output_path = pdf_path.rsplit('.', 1)[0] + '_extracted'
            try:
                if OPENPYXL_AVAILABLE:
                    output_path += '.xlsx'
                    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                        # Save text data
                        if text_data:
                            text_df = pd.DataFrame(text_data)
                            text_df.to_excel(writer, sheet_name='Text', index=False)
                        
                        # Save image OCR data
                        if image_data:
                            image_df = pd.DataFrame(image_data)
                            image_df.to_excel(writer, sheet_name='Images', index=False)
                        
                        # Save table data with proper columns
                        if table_data:
                            for idx, table in enumerate(table_data):
                                table_df = table["DataFrame"]
                                sheet_name = f"Table_{idx + 1}"[:31]  # Excel sheet name limit
                                table_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Data saved to Excel file: {output_path}")
                else:
                    output_path += '.csv'
                    # Save text data to CSV
                    if text_data:
                        text_df = pd.DataFrame(text_data)
                        text_df.to_csv(output_path.replace('.csv', '_text.csv'), index=False)
                    # Save image data to CSV
                    if image_data:
                        image_df = pd.DataFrame(image_data)
                        image_df.to_csv(output_path.replace('.csv', '_images.csv'), index=False)
                    # Save table data to CSV
                    if table_data:
                        for idx, table in enumerate(table_data):
                            table_df = table["DataFrame"]
                            table_df.to_csv(output_path.replace('.csv', f'_table_{idx + 1}.csv'), index=False)
                    logger.info(f"Data saved to CSV files: {output_path.replace('.csv', '_*.csv')}")
            
            except Exception as e:
                logger.error(f"Error saving data to file: {str(e)}. Data not saved, but extraction completed.")
            
            return result
        
        except Exception as e:
            logger.error(f"Error processing PDF with PyMuPDF: {str(e)}")
            # Fallback to PyPDF2 if available
            if PYPDF2_AVAILABLE:
                try:
                    pdf_reader = PdfReader(pdf_path)
                    result = []
                    for page_num, page in enumerate(pdf_reader.pages):
                        page_key = f"Page {page_num + 1}"
                        page_dict = {
                            "page_no": page_num + 1,
                            "extracted_text": "Not available",
                            "extracted_text_from_image": "Not available",
                            "extracted_tabular_data": "Not available"
                        }
                        text = page.extract_text()
                        if text.strip():
                            page_dict["extracted_text"] = text
                            text_data.append({"Page": page_key, "Text": text})
                        result.append(page_dict)
                    
                        # Save fallback text data
                        output_path = pdf_path.rsplit('.', 1)[0] + '_extracted'
                        if text_data:
                            try:
                                if OPENPYXL_AVAILABLE:
                                    output_path += '.xlsx'
                                    text_df = pd.DataFrame(text_data)
                                    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                                        text_df.to_excel(writer, sheet_name='Text', index=False)
                                    logger.info(f"Fallback data saved to Excel file: {output_path}")
                                else:
                                    output_path += '_text.csv'
                                    text_df = pd.DataFrame(text_data)
                                    text_df.to_csv(output_path, index=False)
                                    logger.info(f"Fallback data saved to CSV file: {output_path}")
                            except Exception as save_error:
                                logger.error(f"Error saving fallback data: {str(save_error)}. Data not saved, but extraction completed.")
                    
                    return result
                
                except Exception as fallback_error:
                    logger.error(f"Fallback extraction with PyPDF2 failed: {str(fallback_error)}")
                    return [{"page_no": 1, "extracted_text": "Not available", "extracted_text_from_image": "Not available", "extracted_tabular_data": "Not available"}]
            else:
                logger.warning("PyPDF2 not available for fallback")
                return [{"page_no": 1, "extracted_text": "Not available", "extracted_text_from_image": "Not available", "extracted_tabular_data": "Not available"}]


    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file"""
        try:
            doc = Document(docx_path)
            full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
            return full_text if full_text else "No text extracted"
        except Exception as e:
            print(f"Error extracting text from DOCX: {str(e)}")
            return "Not available"

    def extract_text_from_txt(self, txt_path):
        """Extract text from a TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            return text if text else "No text extracted"
        except Exception as e:
            print(f"Error extracting text from TXT: {str(e)}")
            return "Not available"
        
    def get_company_json_from_gemini(self, company_document=""):

        """Uses gemini api to get important startup details in json format
        Input: [{"page_no": 1, "extracted_text": "text from page 1", "extracted_text_from_image": "image text from page 1", "extracted_tabular_data": "table data from page 1"}, {...}]
        Output: {"company_name": "name of startup", "sector": "sector of startup", "founded": "2022", "team": "3 founders from IIT Delhi + 10 engineers","market": "Indian SME lending market $50B", "traction": "10,000 users, 20% MoM growth","revenue": "INR 2 Cr ARR", "unique_selling_point": "AI-driven underwriting with 30% lower default rate", "competition": "KreditBee, LendingKart", "risks": "Regulatory hurdles, funding dependency"}
        """
        try:

            prompt=f"{ATTRIBUTE_EXTRACTION_PROMPT} \n\nHere is the extracted content from the startup's document: {company_document} provide the JSON output as specified."
            # Call Gemini API for analysis
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
        
            response_text = response.text.strip()
        
            print("Gemini response:", response_text)

            # Extract and parse JSON from response
            if response_text.startswith('{') and response_text.endswith('}'):
                startup_extracted_data = json.loads(response_text)
            else:
                # Try to find JSON in the response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response_text[start:end]
                    startup_extracted_data = json.loads(json_str)
                else:
                    # Fallback: return error with partial response
                    startup_extracted_data = {
                        "error": "Could not extract valid JSON",
                    }
            return startup_extracted_data

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            # Return fallback structure with error info
            return {
                "error": f"JSON decode error: {str(e)}",
                "company_name": "Unknown",
                "sector": "Unknown",
                "raw_response": response_text[:200] if 'response_text' in locals() else "No response"
            }


            
    def startup_evaluation(self, startup_important_details_json):
        
        """Uses gemini api to evaluate startup based on json input based on 10 parameters
        Input: company_important_details_json {"company_name": "name of startup", "sector": "sector of startup", "founded": "2022", "team": "3 founders from IIT Delhi + 10 engineers","market": "Indian SME lending market $50B", "traction": "10,000 users, 20% MoM growth","revenue": "INR 2 Cr ARR", "unique_selling_point": "AI-driven underwriting with 30% lower default rate", "competition": "KreditBee, LendingKart", "risks": "Regulatory hurdles, funding dependency"}
        Output: {"Sector": {"score": 8, "justification": "High-growth sector with favorable trends"}, "Team_Quality": {"score": 9, "justification": "Experienced team with proven track record"}, ...}
        """
        try:

            prompt=f"{STARTUP_SCORING_PROMPT} \n\nHere is the important details about the startup:\n\n{str(startup_important_details_json)}"
            # Call Gemini API for analysis

            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
        
            response_text = response.text.strip()
        
            print("Gemini response:", response_text)

            # Extract and parse JSON from response
            if response_text.startswith('{') and response_text.endswith('}'):
                startup_score_extracted_data = json.loads(response_text)
            else:
                # Try to find JSON in the response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response_text[start:end]
                    startup_score_extracted_data = json.loads(json_str)
                else:
                    startup_score_extracted_data = {
                        "error": "Could not extract valid JSON",
                    }
            return startup_score_extracted_data

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            return {}
        


    def calculate_final_score_updated(self, evaluation_data) -> dict:
        # Define weightages for each parameter
        weightages = {
            "Team_Quality": 0.15,
            "Market_Size": 0.15,
            "Traction": 0.15,
            "Financials": 0.10,
            "Product_Uniqueness": 0.15,
            "Competitive_Landscape": 0.10,
            "Business_Model_Clarity": 0.10,
            "Risk_Factors": 0.10
        }
        
        # Check if evaluation_data is a dict with 'startup_score' key
        if isinstance(evaluation_data, dict) and "startup_score" in evaluation_data:
            input_data = evaluation_data["startup_score"]
        else:
            input_data = evaluation_data  # Assume it's already the list of parameters
        
        # Process input data to add weightage, weighted_score, and benchmark_weighted_score
        result = []
        for item in input_data:
            parameter = item["Parameter"]
            weight = weightages.get(parameter, 0.10)  # Default weight if not found
            
            # Calculate weighted scores
            weighted_score = item["Score"] * weight
            benchmark_weighted_score = item["Benchmark_normalized"] * weight
            
            # Create new dictionary with all required fields
            updated_item = {
                "Parameter": parameter,
                "Score": item["Score"],
                "Threshold": item["Threshold"],
                "Benchmark_normalized": item["Benchmark_normalized"],
                "Weightage": weight,
                "Weighted_Score": round(weighted_score, 2),
                "benchmark_weighted_score": round(benchmark_weighted_score, 2)
            }
            result.append(updated_item)
        
        # Return the final JSON structure
        return result

    def derive_insight(self, uploaded_files_content, startup_extracted_data, startup_score_normalized, final_score, final_benchmark_score):
        
        """Uses gemini api to identify red and green flags and recommendations
        Input: 
        Output: 
        """
        try:

            prompt=f"{INSIGHT_PROMPT} \n\nHere is the important details about the startup: The text provided from pitch deck and other documents \n\n{str(uploaded_files_content)}  \n\n The important extracted attributes of company from files {str(startup_extracted_data)} \n\the evaluation scores about the startup:\n\n{str(startup_score_normalized)}\n\nHere is the overall score about the startup:\n\n{str(final_score)} against the benchmark score considering top players in similar category which is final benchmark score: {str(final_benchmark_score)} "
            # Call Gemini API for analysis
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
        
            response_text = response.text.strip()
        
            print("Gemini response:", response_text)

            # Extract and parse JSON from response
            if response_text.startswith('{') and response_text.endswith('}'):
                generated_insight = json.loads(response_text)
            else:
                # Try to find JSON in the response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response_text[start:end]
                    generated_insight = json.loads(json_str)
                else:
                    generated_insight = {
                        "error": "Could not extract valid JSON",
                    }
            return generated_insight

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            return {}

    def report_generation(self, startup_data, score_data, overall_score_data, insights_data):
        pass


