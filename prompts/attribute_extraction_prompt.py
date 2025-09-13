ATTRIBUTE_EXTRACTION_PROMPT = """

    I am providing you with text extracted from a pitch deck or business document. Please analyze this content and extract comprehensive company information. Return ONLY a valid JSON object with these fields (set to not available if not found):

output format:

{
  "company_name": "",
  "founded_year": "",
  "sector": "",
  "stage": "",
  "location": "",
  "problem_statement": "",
  "solution_description": "",
  "unique_value_proposition": "",
  "market_analysis": {
    "tam": "",
    "sam": "",
    "som": "",
    "market_growth_rate": ""
  },
  "business_model": {
    "revenue_streams": [],
    "pricing_strategy": "",
    "customer_acquisition_cost": "",
    "lifetime_value": ""
  },
  "traction": {
    "user_metrics": {
      "total_users": 0,
      "active_users": 0,
      "growth_rate": ""
    },
    "revenue_metrics": {
      "current_arr": "",
      "monthly_recurring_revenue": "",
      "revenue_growth_rate": ""
    },
    "key_milestones": []
  },
  "team": {
    "founders": [],
    "key_members": [],
    "advisors": []
  },
  "competition": {
    "competitors": [],
    "competitive_advantages": []
  },
  "financials": {
    "current_revenue": "",
    "projected_revenue": {
      "year1": "",
      "year2": "",
      "year3": ""
    },
    "burn_rate": "",
    "runway": ""
  },
  "funding_ask": {
    "amount": "",
    "valuation": "",
    "use_of_funds": []
  },
  "risks_and_mitigations": [],
  "exit_strategy": ""
}

I am providing you with the following content to analyze:

- Extracted Text data from pitch deck page no wise
- Extracted Text from images in pitch deck page no wise
- Extracted Tabular data from pitch deck page no wise
- Call transcript of any audio/video content if available
- founder notes if available

"""