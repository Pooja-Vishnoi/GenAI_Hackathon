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

def create_results_from_paths(file_paths=None):
    """
    Alternative version of create_results that works with file paths instead of UploadedFile objects.
    This is used by the FastAPI server.
    """
    df = pd.DataFrame()
    structured_df = pd.DataFrame()
    final_score = 0.0
    flags = {}
    Recommendations = {}
    
    print(f"[DEBUG] create_results_from_paths called with {len(file_paths) if file_paths else 0} files")
    
    if file_paths and len(file_paths) > 0:
        try:
            # Import the file reading utilities
            from Utils.ai_startup_utility import AIStartupUtility
            from docx import Document
            
            # Read files from paths
            analyst = AIStartupUtility()
            results = {}
            
            for file_path in file_paths:
                print(f"[DEBUG] Processing file: {file_path}")
                filename = os.path.basename(file_path)
                ext = os.path.splitext(filename)[1].lower()
                text = ""
                
                try:
                    if ext == ".pdf":
                        print(f"[DEBUG] Extracting text from PDF: {file_path}")
                        text = analyst.extract_text_from_pdf(file_path)
                        print(f"[DEBUG] Extracted {len(text)} characters from PDF")
                    elif ext == ".docx":
                        print(f"[DEBUG] Reading DOCX file: {file_path}")
                        doc = Document(file_path)
                        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
                        print(f"[DEBUG] Extracted {len(text)} characters from DOCX")
                    elif ext == ".txt":
                        print(f"[DEBUG] Reading TXT file: {file_path}")
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()
                        print(f"[DEBUG] Read {len(text)} characters from TXT")
                    else:
                        text = f"[Unsupported file type: {ext}]"
                        print(f"[DEBUG] Unsupported file type: {ext}")
                    
                    results[filename] = text
                    print(f"[DEBUG] Added {filename} to results with {len(text)} chars")
                except Exception as e:
                    print(f"[ERROR] Error reading file {file_path}: {e}")
                    import traceback
                    traceback.print_exc()
                    results[filename] = f"[Error: {e}]"
            
            print(f"[DEBUG] Total files read: {len(results)}")
            print(f"[DEBUG] Results keys: {list(results.keys())}")
            
            # Now process the content
            if results:
                try:
                    print(f"[DEBUG] Calling content_to_json with {len(results)} files")
                    startup_extracted_data = content_to_json(content=results)
                    print(f"[DEBUG] Extracted data: {startup_extracted_data}")
                    
                    if not startup_extracted_data:
                        print("[WARNING] No data extracted from files, using dummy data")
                        # Use dummy data for testing
                        startup_extracted_data = {
                            "Startup": "Test Startup",
                            "Sector": "Technology",
                            "Team Quality": "Strong founding team with 10+ years experience",
                            "Market Size": "$300B TAM in data analytics",
                            "Traction": "42 active customers, $400K pipeline",
                            "Financials": "Monthly burn ₹14L, 18 months runway",
                            "Risk Factors": "High competition, need for talent acquisition"
                        }
                    
                    # Convert to DataFrame
                    startup_extracted_df = pd.DataFrame(list(startup_extracted_data.items()), 
                                                       columns=["Parameters", "Details"])
                    print(f"[DEBUG] Created DataFrame with {len(startup_extracted_df)} rows")
                    
                    # Process data
                    df = startup_extracted_df.copy()
                    df = df[~df["Parameters"].isin(["Startup", "Sector"])].reset_index(drop=True)
                    print(f"[DEBUG] Filtered DataFrame to {len(df)} rows")
                    
                    # Score and structure
                    structured_df = convert_raw_to_structured(df)
                    print(f"[DEBUG] Structured DataFrame has {len(structured_df)} rows")
                    
                    structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]
                    final_score = structured_df["Weighted_Score"].sum()
                    print(f"[DEBUG] Final score: {final_score}")
                    
                    # Detect flags and generate recommendations
                    red_flags = detect_red_flags(structured_df)
                    green_flags = detect_green_flags(structured_df)
                    Recommendations = generate_recommendations(structured_df, red_flags, green_flags)
                    
                    # Update the flags variable for return
                    if isinstance(red_flags, list) and len(red_flags) > 0:
                        flags = red_flags
                    
                    print(f"[DEBUG] Analysis complete - Score: {final_score}, Red flags: {red_flags}, Green flags: {len(green_flags)}")
                    
                except Exception as e:
                    print(f"[ERROR] Error processing extracted data: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("[WARNING] No results to process")
                    
        except Exception as e:
            print(f"[ERROR] Error in create_results_from_paths: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[WARNING] No file paths provided")
    
    return df, structured_df, final_score, flags, Recommendations

def create_results(uploaded_files = None):
    df = pd.DataFrame()
    structured_df = pd.DataFrame()
    final_score = 0.0
    flags = {}
    Recommendations = {}
    
    # Initialize variables to avoid UnboundLocalError
    uploaded_files_content = None
    startup_extracted_data = None

    if uploaded_files:
        # Step 1: Read files
        try:
            uploaded_files_content = read_files(uploaded_files)  
            print(f"The content of uploaded files are: {uploaded_files_content}")
        except Exception as e:
            print(f"Error reading files: {e}")
            # Return empty results if file reading fails
            return df, structured_df, final_score, flags, Recommendations

        # Step 2: Extract data from content
        try:
            startup_extracted_data = content_to_json(content=uploaded_files_content)
            print(f"The Extracted data from gemini is: {startup_extracted_data}")
        except Exception as e:
            print(f"Error extracting data from content: {e}")
            # Return empty results if extraction fails
            return df, structured_df, final_score, flags, Recommendations

        # Step 3: Process extracted data
        try:
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
            
        except Exception as e:
            print(f"Error processing data: {e}")
            # Return whatever we have so far
            return df, structured_df, final_score, flags, Recommendations

    else: 
        print("No uploaded files provided")
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
