import logging
import os

log_file = os.path.join(os.path.dirname(__file__), "app.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True  # <-- This is important for Streamlit!
)
logger = logging.getLogger()


import pandas as pd
from Utils.utils import read_files, read_file
from Utils.pdf_file_reader import content_to_json
from Utils.structured_2_scored_data import convert_raw_to_structured
from Utils.final_score import final_score
# import logging
# import os
import json
with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    config = json.load(f)

# START LOGGING
# log_file = os.path.join(os.path.dirname(__file__), "app.log")
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_file, mode='a', encoding='utf-8'),
#         logging.StreamHandler()  # Optional: also log to console
#     ]
# )

# logger = logging.getLogger(__name__)
# STOP LOGGING


from Utils.ai_startup_utility import AIStartupUtility


# Setting up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

GEMINI_MODEL = config.get("gemini_model", "gemini-2.0-flash")
TEMPERATURE = config.get("temperature", 0.7)
MAX_OUTPUT_TOKENS = config.get("max_output_tokens", 500)

from agents.investor_agent import investor_recommendation_agent, investor_recommendation_executor

# def create_results(uploaded_files = None):
#     df = pd.DataFrame()
#     structured_df = pd.DataFrame()
#     final_score = 0.0
#     flags = {}
#     Recommendations = {}

#     if uploaded_files:

#         try:
#             uploaded_files_content = read_files(uploaded_files)  
#             print(f"The content of uploaded files are: {uploaded_files_content}")
#         except Exception as e:
#             print(e)

#         try:
#             startup_extracted_data = content_to_json(content=uploaded_files_content)
#             print(f"The Extracted data from gemini is: {startup_extracted_data}")
#         except Exception as e:
#             print(e)

#         # Move all details from json to dataframe to populate on dashboard
#         startup_extracted_df = pd.DataFrame(list(startup_extracted_data.items()), columns=["Parameters", "Details"])

#         print(startup_extracted_df)

#         # for further processing we will keep only evaluating parameters and remove others like startup name, sector etc
#         df = startup_extracted_df.copy()
#         df = df[~df["Parameters"].isin(["Startup", "Sector"])].reset_index(drop=True)

#         # Score each parameter between 1 to 10 based on some defined logic, 
#         # pull benchmark data from bigquery for this sector and add here
#         # add weightage and threshold in df
#         structured_df = convert_raw_to_structured(df)
#         print(structured_df)

#         # Convert normalized scores to weighted scores based on weightage of each parameter
#         structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]

#         # Final weighted score
#         final_score = structured_df["Weighted_Score"].sum()
#         print(structured_df)
#         print(round(final_score, 2))

#         # Identify Red Flags
#         red_flags = detect_red_flags(structured_df)
#         green_flags = detect_green_flags(structured_df)

#         # Generate recommendations
#         Recommendations = generate_recommendations(structured_df, red_flags, green_flags)

#     else: 
#         print("not uploaded files")
#     """Create dummy results dataframe with 10 rows × 5 columns"""

#     return df, structured_df, final_score, flags, Recommendations

def create_results(uploaded_files=None):
    df = pd.DataFrame()
    startup_extracted_df = pd.DataFrame()
    structured_df = pd.DataFrame()
    final_score = 0.0
    flags = {}
    Recommendations = {}
    uploaded_files_content = {}

    if uploaded_files:
        
            logger.info("Attempting to read uploaded files...")
            uploaded_files_content = read_files(uploaded_files)
            logger.info(f"Successfully read the uploaded files: {uploaded_files_content}")
        
            # logger.error(f"Error reading uploaded files: {e}")
            # return df, structured_df, final_score, flags, Recommendations
            # return df, structured_df, final_score, flags, Recommendations, uploaded_files_content
        
            logger.info("Converting content to JSON...")
            startup_extracted_data = content_to_json(content=uploaded_files_content)

            # sending sample data to test rest of the flow in case if failed to read file
            if startup_extracted_data["company_name"] == "Not available":
                logger.warning("Using sample data as extracted data is incomplete.")
                startup_extracted_data = {
                    "company_name": "Used Dummy input data for evaluation  as error reading input files",
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

            # Add uploaded_files_content to extracted data
            # startup_extracted_data["uploaded_files_content"] = uploaded_files_content

            # startup_final_data = {
            #     "files_content": uploaded_files_content,
            #     "extracted_data": startup_extracted_data
            # }
            # logger.info(f"Extracted data from Gemini: {startup_extracted_data}")
        
            # logger.error(f"Error extracting content from Gemini: {e}")
            # return df, structured_df, final_score, flags, Recommendations

        # Move all details from json to dataframe to populate on dashboard
    
            logger.info("Converting extracted data to DataFrame...")
            startup_extracted_df = pd.DataFrame(list(startup_extracted_data.items()), columns=["Parameters", "Details"])
            logger.debug(f"Extracted DataFrame Keys: {startup_extracted_df.keys()}")

            # logger.error(f"Error converting extracted data to DataFrame: {e}")
            # return df, structured_df, final_score, flags, Recommendations

        # Filter and reset DataFrame
            logger.info("Processing DataFrame to filter evaluation parameters...")
            df = startup_extracted_df.copy()
            df = df[~df["Parameters"].isin(["Startup", "Sector"])].reset_index(drop=True)
            logger.debug(f"Filtered DataFrame: {df}")
            # logger.error(f"Error processing DataFrame: {e}")
            # return df, structured_df, final_score, flags, Recommendations

        # Convert to structured data
            logger.info("Converting raw data to structured data...")
            # structured_df = convert_raw_to_structured(df)
            ai_startup_utility_obj =AIStartupUtility()
            startup_score  = ai_startup_utility_obj.startup_evaluation(startup_extracted_data)
            logger.info(f"startup score: {startup_score}")
            startup_score_normalized=ai_startup_utility_obj.calculate_final_score_updated(startup_score)
            print(startup_score_normalized)

            structured_df= pd.DataFrame(startup_score_normalized)
            # print(structured_df)

            # structured_df = convert_raw_to_structured(df)
            # print(structured_df)

            # logger.info(f"Structured DataFrame: {structured_df}")
            # logger.error(f"Error converting raw data to structured data: {e}")
            # return df, structured_df, final_score, flags, Recommendations

        # Calculate weighted score
            logger.info("Calculating weighted scores...")
            structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]
            final_score = structured_df["Weighted_Score"].sum()
            logger.info(f"Final weighted score calculated: {round(final_score, 2)}")
            final_benchmark_score = structured_df["benchmark_weighted_score"].sum()
            logger.info(f"Final weighted score calculated: {round(final_benchmark_score, 2)}")
        # except Exception as e:
        #     logger.error(f"Error calculating weighted score: {e}")
        #     return df, structured_df, final_score, flags, Recommendations

        # Identify Red Flags and Green Flags
        # try:
            logger.info("Detecting red and green flags...")
            # red_flags = detect_red_flags(structured_df)      # [red_flags_points[], red_flags_reference[]]
            # green_flags = detect_green_flags(structured_df)
            # logger.info(f"Red Flags: {red_flags}")
            # logger.info(f"Green Flags: {green_flags}")
            ai_startup_utility_obj =AIStartupUtility()
            flags = ai_startup_utility_obj.derive_insight(uploaded_files_content, startup_extracted_data, startup_score_normalized, final_score, final_benchmark_score)
            print(" =====================  flags : ", flags)

            red_flags_list = flags.get("red_flags", [])         # [{'description': 'str', 'reference': 'str'}, ...]
            green_flags_list = flags.get("green_flags", [])     # [{'description': 'str', 'reference': 'str'}, ...]

            red_flags = [item['description'] for item in red_flags_list]
            green_flags = [item['description'] for item in green_flags_list]

            logger.info(f"flags: {flags}")
        # except Exception as e:
        #     logger.error(f"Error detecting flags: {e}")
        #     return df, structured_df, final_score, flags, Recommendations

        # Generate recommendations
        # try:
            logger.info("Generating recommendations...")
            Recommendations = generate_recommendations(structured_df, red_flags, green_flags)
            logger.info(f"Recommendations generated: {Recommendations}")
        # except Exception as e:
        #     logger.error(f"Error generating recommendations: {e}")
        #     return df, structured_df, final_score, flags, Recommendations

    else:
        logger.warning("No uploaded files provided.")
        # exit()

    
           

    return df, structured_df, final_score, flags, Recommendations, uploaded_files_content
    # return df, structured_df, final_score, flags, Recommendations


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

def analyze_results(uploaded_files_content, structured_df):
    """Run all analysis steps on the DataFrame"""
    # Convert normalized scores to weighted scores based on weightage of each parameter

    print(structured_df)

    structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]
    
    # Final weighted score
    final_score = structured_df["Weighted_Score"].sum()
    print(structured_df)
    print(round(final_score, 2))

    # Identify Red Flags
    # red_flags = detect_red_flags(structured_df)
    # green_flags = detect_green_flags(structured_df)

    startup_extracted_data = content_to_json(content=uploaded_files_content)
    startup_score_normalized = structured_df.to_dict(orient="records")
    final_score = structured_df["Weighted_Score"].sum()
    final_benchmark_score = structured_df["benchmark_weighted_score"].sum()

    ai_startup_utility_obj =AIStartupUtility()
    flags = ai_startup_utility_obj.derive_insight(uploaded_files_content, startup_extracted_data, startup_score_normalized, final_score, final_benchmark_score)
    print(" =====================  flags : ", flags)

    red_flags_list = flags.get("red_flags", [])
    green_flags_list = flags.get("green_flags", [])

    red_flags = [item['description'] for item in red_flags_list]
    green_flags = [item['description'] for item in green_flags_list]

    # Generate recommendations
    Recommendations = generate_recommendations(structured_df, red_flags, green_flags)
    return final_score, flags, Recommendations
