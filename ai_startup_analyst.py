"""


install required packages:


pip install pymupdf pytesseract Pillow pandas pdfplumber PyPDF2 google-genai python-dotenv


"""


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
from prompts.attribute_extraction_prompt import ATTRIBUTE_EXTRACTION_PROMPT
from prompts.startup_scoring_prompt import STARTUP_SCORING_PROMPT
from prompts.insight_prompt import INSIGHT_PROMPT

import json
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class AIStartupAnalyst:

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
        
        try:
            # Open the PDF file using PyMuPDF
            doc = fitz.open(pdf_path)
            
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
                page_text = "\n".join([block[4].strip() for block in blocks if block[6] == 0])  # Text only, skip images
                if page_text.strip():
                    page_dict["extracted_text"] = page_text
                    text_data.append({"Page": page_key, "Text": page_text})
                
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
                            print(f"Error processing image {img_index + 1} on page {page_num + 1}: {str(e)}")
                    if image_texts:
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
                    print(f"Error extracting tables with pdfplumber: {str(e)}. Skipping table extraction.")
            else:
                print("Table extraction skipped: pdfplumber not installed.")
            
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
                    print(f"Data saved to Excel file: {output_path}")
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
                    print(f"Data saved to CSV files: {output_path.replace('.csv', '_*.csv')}")
            
            except Exception as e:
                print(f"Error saving data to file: {str(e)}. Data not saved, but extraction completed.")
            
            return result
        
        except Exception as e:
            print(f"Error processing PDF with PyMuPDF: {str(e)}")
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
                                print(f"Fallback data saved to Excel file: {output_path}")
                            else:
                                output_path += '_text.csv'
                                text_df = pd.DataFrame(text_data)
                                text_df.to_csv(output_path, index=False)
                                print(f"Fallback data saved to CSV file: {output_path}")
                        except Exception as save_error:
                            print(f"Error saving fallback data: {str(save_error)}. Data not saved, but extraction completed.")
                    
                    return result
                
                except Exception as fallback_error:
                    print(f"Fallback extraction with PyPDF2 failed: {str(fallback_error)}")
                    return [{"page_no": 1, "extracted_text": "Not available", "extracted_text_from_image": "Not available", "extracted_tabular_data": "Not available"}]
            else:
                print("PyPDF2 not available for fallback")
                return [{"page_no": 1, "extracted_text": "Not available", "extracted_text_from_image": "Not available", "extracted_tabular_data": "Not available"}]

        
    def get_company_json_from_gemini(self, pitch_deck_content="", call_transcript="", founder_updates="", email_content=""):

        """Uses gemini api to get important startup details in json format
        Input: [{"page_no": 1, "extracted_text": "text from page 1", "extracted_text_from_image": "image text from page 1", "extracted_tabular_data": "table data from page 1"}, {...}]
        Output: {"company_name": "name of startup", "sector": "sector of startup", "founded": "2022", "team": "3 founders from IIT Delhi + 10 engineers","market": "Indian SME lending market $50B", "traction": "10,000 users, 20% MoM growth","revenue": "INR 2 Cr ARR", "unique_selling_point": "AI-driven underwriting with 30% lower default rate", "competition": "KreditBee, LendingKart", "risks": "Regulatory hurdles, funding dependency"}
        """
        try:

            prompt=f"{ATTRIBUTE_EXTRACTION_PROMPT} \n\nHere is the extracted content from the pitch deck or business document:\n\n{pitch_deck_content}\n\n{call_transcript}\n\n{founder_updates}\n\n{email_content}\n\nPlease provide the JSON output as specified."
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
        
    def calculate_final_score(self, evaluation_data):
        """
        Input: {'scores': {'Sector': {'score': 9, 'justification': 'The aquaculture sector in India is massive (2nd largest globally) and growing rapidly at a 10% CAGR, faster than GDP. The startup addresses critical issues like credit access and transparency, aligning with broader fintech and sustainable development trends in a vital industry.'}, 'Team_Quality': {'score': 9, 'justification': "The team is exceptionally strong and well-rounded, featuring a serial entrepreneur CEO (IIT Kanpur, Stanford), and highly experienced key members with deep domain expertise in aquaculture, agri-input sales, seafood value chains, fintech, AI/ML, and data science (e.g., ex-TATA Rallis, Walmart, Urban Company, MIT Tech Review awardee). The skill sets are highly complementary and directly relevant to the complex problem Aquaconnect is solving. The only minor gap is no listed advisors and one key role 'currently onboarding'."}, 'Market_Size': {'score': 9, 'justification': "India's aquaculture market represents a massive TAM, being the 2nd largest global producer with 5 million farmers and significant reserves. The sector's 10% CAGR confirms it's a large and expanding market with substantial potential, especially given India's position as the largest shrimp exporter."}, 'Traction': {'score': 9, 'justification': 'Traction is exceptionally strong, with revenue growing 9X over 6 months (Jan-Nov 2021), reaching an impressive ~$6.5M ARR. Key milestones include generating $15M in economic value for farmers and achieving significant reductions in feed usage. While direct user counts for partners/buyers seem modest for Series A, the rapid revenue growth and tangible impact metrics clearly validate the product-market fit and execution.'}, 'Financials': {'score': 6, 'justification': "Current revenue is strong at ~$6.5M ARR (Nov 2021). The projected annualized revenue of $12M - $16M by March 2024 seems realistic and achievable given the current growth. However, critical information such as burn rate and runway is not provided, making it difficult to fully assess the startup's financial health and long-term sustainability without further data."}, 'Product_Uniqueness': {'score': 9, 'justification': 'Aquaconnect offers a highly innovative, full-stack fintech platform that integrates inputs, outputs, and credit across the entire aquaculture value chain. Its unique value proposition lies in leveraging proprietary farm-level data (GIS remote sensing, ground teams) to build a robust data science and underwriting engine, creating a significant data moat and enabling effective credit solutions in an underserved market.'}, 'Competitive_Landscape': {'score': 7, 'justification': "While the list of direct competitors is notably empty (a potential red flag if not thoroughly analyzed), Aquaconnect's stated competitive advantages are very strong: a full-stack integrated platform, proprietary farm-level data for credit underwriting, and significant social impact. This suggests they are either pioneering a category or operating with a highly differentiated approach in a fragmented market with inadequate existing solutions."}, 'Business_Model_Clarity': {'score': 7, 'justification': 'The business model is clear with diversified revenue streams from trade margins (2-20%) on GMV and financing margins (~18-25% APR) from BNPL products. The pricing strategy is also detailed. The model appears scalable, and the indication of improved blended take rates through financing is positive. However, the absence of explicit Customer Acquisition Cost (CAC) and Lifetime Value (LTV) metrics prevents a comprehensive assessment of unit economics.'}, 'Risk_Factors': {'score': 1, 'justification': 'No specific risk factors or mitigation strategies are identified in the provided information. This is a significant red flag, as every startup faces inherent risks (market, regulatory, operational, technological, financial). The lack of this critical assessment suggests either an oversight or an unwillingness to address potential challenges, increasing the perceived overall risk level.'}}}
        
        Output: final_score json based on weightage of each parameter
        """
        weights = {
            "Sector": 5,
            "Team_Quality": 25,
            "Market_Size": 20,
            "Traction": 15,
            "Financials": 10,
            "Product_Uniqueness": 10,
            "Competitive_Landscape": 5,
            "Business_Model_Clarity": 5,
            "Risk_Factors": 5
        }
        import json
        scores = evaluation_data['scores']
        weighted_scores = {}
        total_weighted = 0
        total_weight = 0
        for param, data in scores.items():
            score = data['score']
            weight = weights[param]
            weighted = score * weight
            weighted_scores[param] = {
                'score': score,
                'weight': weight,
                'weighted': weighted
            }
            total_weighted += weighted
            total_weight += weight
        overall_score = total_weighted / total_weight
        result = {
            'weighted_scores': weighted_scores,
            'overall_score': overall_score
        }
        return json.dumps(result, indent=4)
    
    def derive_insight(self, startup_data, score_data, overall_score_data):
        
        """Uses gemini api to identify red and green flags and recommendations
        Input: 
        Output: 
        """
        try:

            prompt=f"{INSIGHT_PROMPT} \n\nHere is the important details about the startup:\n\n{str(startup_data)}\n\nHere is the evaluation scores about the startup:\n\n{str(score_data)}\n\nHere is the overall score about the startup:\n\n{str(overall_score_data)}"
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

if __name__ == "__main__":
    analyst = AIStartupAnalyst()
    pdf_path = "data/presentation_04_05.pdf"
    text_data = analyst.extract_text_from_pdf(pdf_path)
    print(text_data)

    structured_company_info = analyst.get_company_json_from_gemini(pitch_deck_content=str(text_data), call_transcript="", founder_updates="", email_content="")
    print(structured_company_info)

    startup_score = analyst.startup_evaluation(structured_company_info)
    print(startup_score)

    overall_score = analyst.calculate_final_score(startup_score)
    print(overall_score)

    insight_data = analyst.derive_insight(structured_company_info, startup_score, overall_score)
    print(insight_data)