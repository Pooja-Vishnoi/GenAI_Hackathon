ATTRIBUTE_EXTRACTION_PROMPT = """

I am providing you with text extracted from multiple documents by startup with tagged filenames and extracted text from each file. Please analyze this content and extract comprehensive company information. Return ONLY a valid JSON object with these fields (set to not available if not found):
keep the json short & crisp yet informative as per type and details mentrioned in the json


Example output format:


{
  "company_name": "Name of the company: str",
  "sector": "Sector of company : for example finance",
  "founded": "founded year: str for ex 2022",
  "team": "a brief about team and their qualifications and accolades: str",
  "market": "a brief about market: str for ex Indian SME lending market $50B",
  "traction": "a brief about traction : str for ex 10,000 users, 20% MoM growth",
  "revenue": " a brief about revenue for ex: INR 2 Cr ARR",
  "unique_selling_point": "a brief about unique_selling point : str for ex AI-driven underwriting with 30% lower default rate",
  "competition": "a brief of competitive companies: str for ex: KreditBee, LendingKart",
  "risks": "a brief about risks: str for ex Regulatory hurdles, funding dependency"
}


Important: Don't return anything  other than json no explaination or extra text

"""