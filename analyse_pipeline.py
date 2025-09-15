import pandas as pd
from Utils.utils import read_files, read_file
from Utils.pdf_file_reader import content_to_json
from Utils.structured_2_scored_data import convert_raw_to_structured
from Utils.final_score import final_score

import os
import json
with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    config = json.load(f)

GEMINI_MODEL = config.get("gemini_model", "gemini-2.0-flash")
TEMPERATURE = config.get("temperature", 0.7)
MAX_OUTPUT_TOKENS = config.get("max_output_tokens", 500)

from agents.investor_agent import investor_recommendation_agent, investor_recommendation_executor

def create_results(uploaded_files = None):
    df = pd.DataFrame()
    structured_df = pd.DataFrame()
    final_score = 0.0
    flags = {}
    Recommendations = {}

    if uploaded_files:

        # Extract file wise content in dict. pdf part in progress
        uploaded_files_content = read_files(uploaded_files)  

        # convert to standard json parameter format
        startup_extracted_data = content_to_json(uploaded_files_content)

        # Move all details from json to dataframe to populate on dashboard
        startup_extracted_df = pd.DataFrame(list(startup_extracted_data.items()), columns=["Parameters", "Details"])

        print(startup_extracted_df)

        # for further processing we will keep only evaluating parameters and remove others like startup name, sector etc
        df = startup_extracted_df.copy()
        df = df[~df["Parameters"].isin(["Startup", "Sector"])].reset_index(drop=True)

        # Score each parameter between 1 to 10 based on some defined logic, 
        # pull benchmark data from bigquery for this sector and add here
        # add weightage and threshold in df
        structured_df = convert_raw_to_structured(df)
        print(structured_df)

        # Convert normalized scores to weighted scores based on weightage of each parameter
        structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]

        # Final weighted score
        final_score = structured_df["Weighted_Score"].sum()
        print(structured_df)
        print(round(final_score, 2))

        # Identify Red Flags
        red_flags = detect_red_flags(structured_df)
        green_flags = detect_green_flags(structured_df)

        # Generate recommendations
        Recommendations = generate_recommendations(structured_df, red_flags, green_flags)

    else: 
        print("not uploaded files")
    """Create dummy results dataframe with 10 rows × 5 columns"""

    return df, structured_df, final_score, flags, Recommendations
    # return df, pd.DataFrame({
    #     "Column 1": [i+1 for i in range(10)],       # numeric values for chart
    #     "Column 2": [(i+1)*2 for i in range(10)],   # numeric values for chart
    #     "Column 3": [f"Val {i+1}-3" for i in range(10)],
    #     "Column 4 (Editable)": [f"Edit {i+1}-4" for i in range(10)],
    #     "Column 5 (Editable)": [f"Edit {i+1}-5" for i in range(10)],
    # }
    # )

def recalculate_results(df):
    """
    Example recalculation logic.
    Append ✅ to Column 3, return updated df.
    Replace with actual analysis logic.
    """
    df = df.copy()
    df["Column 3"] = df["Column 3"].astype(str) + " ✅"
    return df

def calculate_score(df):
    """Dummy scoring logic"""
    return int(df["Column 1"].sum())

def detect_green_flags(df):
    """Dummy red flag detection"""
    flags = []
    flags = ["Strong founding team", "Large market size"]
    return flags

def detect_red_flags(df):
    """
    Detect red flags row-wise:
    - If Score < Threshold, flag it
    - Store flag with reference Page No
    """
    flags = {}

    for idx, row in df.iterrows():
        param = row.get("Parameter", f"Row {idx}")
        score = row.get("Score")
        threshold = row.get("Threshold")
        # page_no = row.get("Page No", "N/A")   # fallback if missing
        page_no = "Pitch deck 10"

        if pd.notna(score) and pd.notna(threshold) and score < threshold:
            flags[param] = {
                "issue": f"Score {score} < Threshold {threshold}",
                "page": page_no
            }

    # Return structured red flags with both text and reference
    # This provides a consistent format for the UI to consume
    red_flags_points = ["High churn", "Low revenue growth"]
    red_flags_reference = ["Refer page No 1", "Refer page no 3"]
    
    # Combine into a structured format
    red_flags = []
    for point, ref in zip(red_flags_points, red_flags_reference):
        red_flags.append({
            'text': point,
            'reference': ref
        })
    
    # For backward compatibility, also return the list format
    # TODO: Update all consumers to use the structured format
    return [red_flags_points, red_flags_reference]

def generate_recommendations(df, red_flags, green_flags):
    """Dummy recommendations"""

    print(df)

    startup_score = (df["Score"] * df["Weightage"]).sum()
    sector_benchmark_score = (df["Benchmark_normalized"] * df["Weightage"]).sum()

    red_flags = red_flags[0]
    green_flags = green_flags
    category_scores = {"financials": df.loc[df['Parameter'] == 'Financials', 'Score'].values[0], "traction": df.loc[df['Parameter'] == 'Traction', 'Score'].values[0]}

    # Run executor to get recommendations
    recommendations = investor_recommendation_executor(
        startup_score,
        sector_benchmark_score,
        red_flags,
        green_flags,
        category_scores,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS
    )


    return recommendations

def analyze_results(structured_df):
    """Run all analysis steps on the DataFrame"""
    # Convert normalized scores to weighted scores based on weightage of each parameter
    structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]

    # Final weighted score
    final_score = structured_df["Weighted_Score"].sum()
    print(structured_df)
    print(round(final_score, 2))

    # Identify Red Flags
    red_flags = detect_red_flags(structured_df)
    green_flags = detect_green_flags(structured_df)

    # Generate recommendations
    Recommendations = generate_recommendations(structured_df, red_flags, green_flags)
    return final_score, red_flags, Recommendations
