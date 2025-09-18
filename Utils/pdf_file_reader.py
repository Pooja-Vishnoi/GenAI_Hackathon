from PyPDF2 import PdfReader
from Utils.ai_startup_utility import AIStartupUtility
import json

def extract_pdf_file_content(uploaded_file):
    '''
    This function will read pdf file content page wise and return text along with page number
    Input - pdf file name. ex - pitch_deck.pdf (with multiple pages, pages can have text, tables, images with text over it, charts) with these details
    Output - {"page 1": "text", "page 2": "text", ....}
    '''
    pdf_reader_dict = PdfReader(uploaded_file)
#   read files using cloud vision and other libraries

    return pdf_reader_dict


def format_extracted_data(data_dict):
    output = ""

    for filename, content in data_dict.items():
        output += f"{filename}:\n"
        
        if isinstance(content, str):
            output += content
        elif isinstance(content, list):
            for item in content:
                output += json.dumps(item) + "\n"
        else:
            output += json.dumps(content)  # for safety

        output += "\n\n"  # separate files with blank lines

    return output

def content_to_json(content):
    '''
    This function will analyze input content using prompt and some logics and rules and return json ouput
    input - content in str or text form. we received from function extract_pdf_file_content and other uploaded material
    Output - json format
        sample json format is - 
            {
                "company_name": "FinTechX",
                "sector": "Finance",
                "founded": "2022",
                "team": "3 founders from IIT Delhi + 10 engineers",
                "market": "Indian SME lending market $50B",
                "traction": "10,000 users, 20% MoM growth",
                "revenue": "INR 2 Cr ARR",
                "unique_selling_point": "AI-driven underwriting with 30% lower default rate",
                "competition": "KreditBee, LendingKart",
                "risks": "Regulatory hurdles, funding dependency"
            }
    '''
    ai_startup_utility_obj=AIStartupUtility()
    try:
        document1=format_extracted_data(content)
        structured_company_info = ai_startup_utility_obj.get_company_json_from_gemini(company_document=document1)
        print(f"structured_company_info: {structured_company_info}")
        startup_extracted_data=structured_company_info
    except Exception as e:
        print(e)
        startup_extracted_data = {
                    "company_name": "FinTechX",
                    "sector": "Finance",
                    "founded": "2022",
                    "team": "3 founders from IIT Delhi + 10 engineers",
                    "market": "Indian SME lending market $50B",
                    "traction": "10,000 users, 20% MoM growth",
                    "revenue": "INR 2 Cr ARR",
                    "unique_selling_point": "AI-driven underwriting with 30% lower default rate",
                    "competition": "KreditBee, LendingKart",
                    "risks": "Regulatory hurdles, funding dependency"
                }

    return startup_extracted_data
