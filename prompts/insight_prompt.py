INSIGHT_PROMPT="""

I am  providing you with detailed information about a startup, including its sector, team, market, traction, financials, product uniqueness, competition, business model, and risks.
and we have evaluated the startup on various parameters based on this information and also justification has been given
and final overall score of the startup based on weighted average of all parameters.

Based on this information, please identify key red flags and green flags for the startup, and provide actionable recommendations for investors to make investing decisions basically you are an ai startup analyst providing this information to investors to may decisions wheter the startup is investible or not.

provide your response in the following JSON format:


{
    "Red_Flags": ["red flag 1", "red flag 2", "..."],
    "Green_Flags": ["green flag 1", "green flag 2", "..."],
    "Recommendations": ["recommendation 1", "recommendation 2", "..."]
}

"""