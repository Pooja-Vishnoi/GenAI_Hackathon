from PyPDF2 import PdfReader

def extract_pdf_file_content(uploaded_file):
    '''
    This function will read pdf file content page wise and return text along with page number
    Input - pdf file name. ex - pitch_deck.pdf (with multiple pages, pages can have text, tables, images with text over it, charts) with these details
    Output - {"page 1": "text", "page 2": "text", ....}
    '''
    pdf_reader_dict = PdfReader(uploaded_file)
#   read files using cloud vision and other libraries

    return pdf_reader_dict


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

    # Parse content and convert into json format as below and return 
    # startup_extracted_data = ..... content .....

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
