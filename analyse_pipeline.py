import pandas as pd
from Utils.utils import read_files, read_file
from Utils.pdf_file_reader import content_to_json
from Utils.structured_2_scored_data import convert_raw_to_structured
from Utils.final_score import final_score

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
        flags = detect_red_flags(structured_df)

        # Generate recommendations
        Recommendations = generate_recommendations(structured_df)

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

# def detect_red_flags(df):
#     """Dummy red flag detection"""
#     flags = []
#     if (df["Column 2"] > 15).any():
#         flags.append("Some Column 2 values exceed threshold (15).")
#     if df["Column 4 (Editable)"].astype(str).str.contains("bad", case=False).any():
#         flags.append("Negative keyword found in Column 4.")
#     return flags

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

    # return flags
    return ["Team Score is less than threshold.           Refer page No 1 ", "Financial Score is less than benchmark     Refer page no 3"]

def generate_recommendations(df):
    """Dummy recommendations"""
    recs = []
    if df["Weighted_Score"].mean() < 5:
        recs.append("Improve Column 1 values to increase overall performance.")
    recs.append("Review edits in Columns 4 and 5 for accuracy.")
    return recs

def analyze_results(structured_df):
    """Run all analysis steps on the DataFrame"""
    # Convert normalized scores to weighted scores based on weightage of each parameter
    structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]

    # Final weighted score
    final_score = structured_df["Weighted_Score"].sum()
    print(structured_df)
    print(round(final_score, 2))

    # Identify Red Flags
    flags = detect_red_flags(structured_df)

    # Generate recommendations
    Recommendations = generate_recommendations(structured_df)
    return final_score, flags, Recommendations
