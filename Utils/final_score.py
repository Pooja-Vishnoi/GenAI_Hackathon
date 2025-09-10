import pandas as pd

def final_score(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw extracted DataFrame (Parameters, Details format)
    into structured scoring DataFrame in long format (rows = parameters).
    """

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

    # Step 1: Convert long → wide
    wide_df = raw_df.set_index("Parameter").T
    wide_df.columns = wide_df.columns.str.lower()
    wide_df = wide_df.rename(columns={"startup": "company_name"})


    # Step 2: Convert wide → long
    structured_df = pd.DataFrame(wide_df).melt(
        var_name="Parameter",
        value_name="Score"
    )

    # Step 3: Add Weightage and Threshold by mapping
    structured_df["Weightage"] = structured_df["Parameter"].map(weightages)
    structured_df["Threshold"] = structured_df["Parameter"].map(thresholds)

    return structured_df
