import pandas as pd
import json

# df_startups = pd.read_csv("data/startup_parameters.csv")
# df_startups.columns = df_startups.columns.str.strip()
# print(df_startups.columns)

df_benchmarks = pd.read_csv("data/sector_benchmarks.csv")
df_benchmarks.columns = df_benchmarks.columns.str.strip()
print(df_benchmarks.columns)

def clean_dict(record):
    cleaned = {}
    for k, v in record.items():
        key = k.strip() if isinstance(k, str) else k
        if isinstance(v, str):
            val = v.strip()
            if val.replace(".", "", 1).isdigit():
                v = float(val) if "." in val else int(val)
            else:
                v = val
        cleaned[key] = v
    return cleaned


def calculate_final_score(data_normalized: dict, weightages: dict, thresholds: dict = None) -> dict:
    """
    Calculate weighted score for each parameter and final score.

    Args:
        data_normalized (dict): Dictionary with parameter -> score (0-10).
        weightages (dict): Dictionary with parameter -> weight (sum = 1.0).

    Returns:
        dict: Dictionary containing individual weighted scores and final score.
    """
    weighted_score = 0.0
    scores = {}
    penalties = []
    flags = []
    final_score = 0.0

    
    sector = data_normalized["Sector"]

    benchmark_row = df_benchmarks[df_benchmarks["Sector"].str.strip().str.lower() == sector.lower()]
    if benchmark_row.empty:
        return {"error": f"No benchmark found for sector {sector}"}
    benchmark_dict = clean_dict(benchmark_row.to_dict(orient="records")[0])


    for param, value in data_normalized.items():

        if param in weightages:
            try:
                value = float(value)  # ensure numeric
            except (ValueError, TypeError):
                value = 0.0

            weight = float(weightages.get(param, 0))
            param_score = value * weight
            scores[param] = round(param_score, 2)
            weighted_score += param_score
        else:
            scores[param] = '-'

        if thresholds and param in thresholds:
            min_req = thresholds[param]
            if value < min_req:
                penalties.append({"parameter": param, "deduction": 1.0})
                flags.append(f"{param} below threshold ({value} < {min_req})")

    # Apply penalties
    final_score = max(0, min(10, weighted_score - sum(p["deduction"] for p in penalties)))
    scores["Final_Score"] = round(final_score, 2)

    return {
        "parameters_normalized": data_normalized,
        "weightages": weightages,
        "thresholds": thresholds, 
        "parameters_score": scores,
        "weighted_score": round(weighted_score, 2),
        "final_score": round(final_score, 2),
        "penalties": penalties,
        "flags": flags
    }

with open("data/data_extracted.json", "r", encoding="utf-8") as ff:
    data_extracted = json.load(ff)

with open("data/data_normalized.json", "r", encoding="utf-8") as f:
    data_normalized = json.load(f)

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

result = calculate_final_score(data_normalized, weightages, thresholds)
result['parameters_extracted'] = data_extracted

with open("data/data_score.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=4))

# ------------------ print in tabular form ---------------------------------------
print(f"{'Parameter':25} {'Normalized':15} {'Score':10}")
print("-" * 55)

for key in result["parameters_normalized"]:
    norm = result["parameters_normalized"].get(key, "-")
    weightage = result["weightages"].get(key, "-")
    threshold = result["thresholds"].get(key, "-")
    score = result["parameters_score"].get(key, "-")
    print(f"{key:25} {str(norm):15} {str(weightage):15} {str(threshold):15} {str(score):10}")

print(f"{'Final_Score':25} {'-':15} {'-':15} {'-':15} {result['parameters_score']['Final_Score']}")
print(result['penalties'])
print(result['flags'])
