'''
Reading structured json and scoring each parameter out of 10 for further evaluation
'''

import re
import json
import pandas as pd

def parse_market_size(market_text: str) -> int:
    """Convert market size text to a 1–10 score."""
    match = re.search(r"(\d+\.?\d*)\s*(B|M)", market_text.upper())
    if not match:
        return 5  # default if not found
    value, unit = float(match.group(1)), match.group(2)
    if unit == "M":
        value *= 1e6
    elif unit == "B":
        value *= 1e9
    
    # Scoring thresholds
    if value >= 1e9: return 10
    if value >= 5e8: return 8
    if value >= 1e8: return 6
    return 4

def parse_traction(traction_text: str) -> int:
    """Convert traction details to a 1–10 score."""
    users_match = re.search(r"(\d+[\d,]*)\s*users", traction_text.lower())
    growth_match = re.search(r"(\d+)%\s*MoM", traction_text)
    
    users = int(users_match.group(1).replace(",", "")) if users_match else 0
    growth = int(growth_match.group(1)) if growth_match else 0
    
    score = 5
    if users > 1e6: score += 3
    elif users > 1e5: score += 2
    elif users > 1e4: score += 1
    
    if growth > 20: score += 2
    elif growth > 10: score += 1
    
    return min(score, 10)

def parse_team(team_text: str) -> int:
    """Heuristic scoring for team background."""
    score = 5
    if "IIT" in team_text.upper() or "IIM" in team_text.upper():
        score += 3
    if "ex-" in team_text.lower() or "mnc" in team_text.lower():
        score += 2
    return min(score, 10)

# def convert_raw_to_structured(raw_json: dict) -> dict:
#     """Convert raw extracted JSON into structured startup_input.json"""
#     structured = {
#         "Startup": raw_json.get("company_name", "Unknown"),
#         "Sector": raw_json.get("sector", "NA"),
#         "Team_Quality": parse_team(raw_json.get("team", "")),
#         "Market_Size": parse_market_size(raw_json.get("market", "")),
#         "Traction": parse_traction(raw_json.get("traction", "")),
#         "Financials": 7 if "ARR" in raw_json.get("revenue", "") else 5,
#         "Product_Uniqueness": 8 if "AI" in raw_json.get("unique_selling_point", "").upper() else 6,
#         "Competitive_Landscape": 5 if len(raw_json.get("competition", "").split(",")) > 2 else 7,
#         "Business_Model_Clarity": 7,  # placeholder
#         "Risk_Factors": 4 if "regulatory" in raw_json.get("risks", "").lower() else 6
#     }
#     return structured

def convert_raw_to_structured(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw extracted DataFrame (Parameters, Details format)
    into structured scoring DataFrame in long format (rows = parameters).
    """

    # Step 1: Convert long → wide
    wide_df = raw_df.set_index("Parameters").T
    wide_df.columns = wide_df.columns.str.lower()
    wide_df = wide_df.rename(columns={"startup": "company_name"})

    structured_data = []

    for _, row in wide_df.iterrows():
        structured = {
            "Team_Quality": parse_team(row.get("team", "")),
            "Market_Size": parse_market_size(row.get("market", "")),
            "Traction": parse_traction(row.get("traction", "")),
            "Financials": 7 if "ARR" in str(row.get("revenue", "")) else 5,
            "Product_Uniqueness": 8 if "AI" in str(row.get("unique_selling_point", "")).upper() else 6,
            "Competitive_Landscape": (
                5 if len(str(row.get("competition", "")).split(",")) > 2 else 7
            ),
            "Business_Model_Clarity": 7,  # placeholder
            "Risk_Factors": 4 if "regulatory" in str(row.get("risks", "")).lower() else 6
        }
        structured_data.append(structured)

    # Convert to DataFrame
    structured_df = pd.DataFrame(structured_data)

    # ✅ Convert wide → long (rows instead of columns)
    structured_df = structured_df.melt(
        var_name="Parameter",
        value_name="Score"
    )

    benchmark = {
        "Team_Quality": 8.8,
        "Market_Size": 7.9,
        "Traction": 9.2,
        "Financials": 6.7,
        "Product_Uniqueness": 8.3,
        "Competitive_Landscape": 7.7,
        "Business_Model_Clarity": 6.5,
        "Risk_Factors": 5.9
    }

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

    thresholds = {
        "Team_Quality": 3,
        "Market_Size": 3,
        "Traction": 3,
        "Financials": 3,
        "Product_Uniqueness": 3,
        "Competitive_Landscape": 3,
        "Business_Model_Clarity": 3,
        "Risk_Factors": 3
    }

    # Step 3: Add benchmark, Weightage and Threshold by mapping
    structured_df["Threshold"] = structured_df["Parameter"].map(thresholds)
    structured_df["Benchmark_normalized"] = structured_df["Parameter"].map(benchmark)
    structured_df["Weightage"] = structured_df["Parameter"].map(weightages)
    
    

    return structured_df


# with open("data/data_extracted.json", "r", encoding="utf-8") as f:
#     extracted_json = json.load(f)

# structured_json = convert_raw_to_structured(extracted_json)

# with open("data/data_normalized.json", "w") as f:
#     json.dump(structured_json, f, indent=2)

# print(json.dumps(structured_json, indent=2))
