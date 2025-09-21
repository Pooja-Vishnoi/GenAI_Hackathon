STARTUP_SCORING_PROMPT = """
please evaluate the startup based on the following 10 parameters, scoring each from 1 to 10, and provide a brief justification for each score. Return ONLY a valid JSON object with these fields:


Evaluation criteria:

{
  "parameters": [
    {
      "name": "Sector",
      "description": "Evaluate the attractiveness of the sector based on growth potential, relevance to current trends, and alignment with broader economic or technological shifts. Use data from 'sector', 'market_analysis' (including growth rate), and 'problem_statement' in the JSON.",
      "sub_criteria": [
        "Sector growth rate and maturity",
        "Alignment with megatrends (e.g., sustainability, AI, health tech)",
        "Regulatory environment and barriers"
      ],
      "scoring_rubric": "1-3: Declining or saturated sector with high barriers; 4-6: Stable sector with moderate growth; 7-10: High-growth sector with favorable trends and low barriers."
    },
    {
      "name": "Team_Quality",
      "description": "Assess the experience, skills, and track record of the team. Draw from 'team' section including founders, key_members, and advisors. Prioritize relevant industry experience, past successes, and complementary skills.",
      "sub_criteria": [
        "Founders' background and expertise",
        "Key team members' roles and experience",
        "Advisors' relevance and network",
        "Team completeness and diversity"
      ],
      "scoring_rubric": "1-3: Inexperienced team with gaps in key skills; 4-6: Solid but unproven team; 7-10: Experienced team with proven track record and strong network."
    },
    {
      "name": "Market_Size",
      "description": "Gauge the total addressable market and growth potential. Use 'market_analysis' fields like TAM, SAM, SOM, and market_growth_rate.",
      "sub_criteria": [
        "Size of TAM/SAM/SOM",
        "Market growth rate",
        "Target market accessibility"
      ],
      "scoring_rubric": "1-3: Small or shrinking market; 4-6: Moderate market size with steady growth; 7-10: Large, expanding market with high potential."
    },
    {
      "name": "Traction",
      "description": "Measure progress and validation. Pull from 'traction' including user_metrics, revenue_metrics, and key_milestones.",
      "sub_criteria": [
        "User growth and engagement",
        "Revenue growth and metrics",
        "Achievement of milestones"
      ],
      "scoring_rubric": "1-3: Minimal traction or stagnation; 4-6: Some growth but inconsistent; 7-10: Strong, accelerating traction with validated metrics."
    },
    {
      "name": "Financials",
      "description": "Review current and projected financial health. Use 'financials' (revenue, projections, burn_rate, runway) and 'funding_ask'.",
      "sub_criteria": [
        "Current revenue and burn rate",
        "Projected revenue realism",
        "Runway and funding needs"
      ],
      "scoring_rubric": "1-3: Poor financials with short runway; 4-6: Break-even potential but risks; 7-10: Solid financials with long runway and realistic projections."
    },
    {
      "name": "Product_Uniqueness",
      "description": "Evaluate innovation and differentiation. Based on 'solution_description', 'unique_value_proposition', and 'competition' (competitive_advantages).",
      "sub_criteria": [
        "Innovation level and IP protection",
        "Clear value proposition",
        "Barrier to adoption"
      ],
      "scoring_rubric": "1-3: Commodity product with no differentiation; 4-6: Some uniqueness but easily replicable; 7-10: Highly innovative with strong moats."
    },
    {
      "name": "Competitive_Landscape",
      "description": "Analyze competitors and advantages. From 'competition' section.",
      "sub_criteria": [
        "Number and strength of competitors",
        "Competitive advantages and moats",
        "Market positioning"
      ],
      "scoring_rubric": "1-3: Highly competitive with dominant players; 4-6: Moderate competition; 7-10: Fragmented market with clear advantages."
    },
    {
      "name": "Business_Model_Clarity",
      "description": "Assess scalability and revenue potential. Use 'business_model' (revenue_streams, pricing_strategy, CAC, LTV).",
      "sub_criteria": [
        "Clarity of revenue streams",
        "Scalability and unit economics (CAC vs. LTV)",
        "Pricing strategy effectiveness"
      ],
      "scoring_rubric": "1-3: Unclear or unsustainable model; 4-6: Defined but unproven; 7-10: Clear, scalable model with positive economics."
    },
    {
      "name": "Risk_Factors",
      "description": "Identify and mitigate risks. From 'risks_and_mitigations' and overall analysis.",
      "sub_criteria": [
        "Key risks identified",
        "Mitigation strategies",
        "Overall risk level"
      ],
      "scoring_rubric": "1-3: High unmitigated risks; 4-6: Some risks with partial mitigations; 7-10: Low risks with strong mitigations."
    }
  ]
}


Finally return a JSON object structured as follows:

{
  "scores": {
    "Sector": {"score": int, "justification": str},
    "Team_Quality": {"score": int, "justification": str},
    "Market_Size": {"score": int, "justification": str},
    "Traction": {"score": int, "justification": str},                                    
    "Financials": {"score": int, "justification": str},
    "Product_Uniqueness": {"score": int, "justification": str},
    "Competitive_Landscape": {"score": int, "justification": str},
    "Business_Model_Clarity": {"score": int, "justification": str},
    "Risk_Factors": {"score": int, "justification": str}
}

"""