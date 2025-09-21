STARTUP_SCORING_PROMPT = """
Please evaluate the startup based on the following 8 parameters, assigning each an integer score from 1 to 10. Use publicly available data and industry context to inform your evaluation. Return a valid JSON object with the specified structure.

**Evaluation Criteria**:

- **Team Quality**: Assess the founding team's experience, skills, cohesion, and ability to execute the startup's vision.
  - Low (1-3): Inexperienced team, lacking critical skills or cohesion.
  - Moderate (4-6): Some relevant experience, with identifiable strengths but gaps in expertise.
  - High (7-10): Highly experienced, cohesive team with a proven track record and strong execution capability.

- **Market Size**: Evaluate the target market's size, growth potential, and scalability.
  - Low (1-3): Small or stagnant market with limited growth potential.
  - Moderate (4-6): Moderately sized market with reasonable growth prospects.
  - High (7-10): Large, rapidly growing market with significant scalability.

- **Traction**: Measure the startup's momentum through customer acquisition, revenue, or other growth metrics.
  - Low (1-3): Minimal or no traction, very early stage with limited evidence of progress.
  - Moderate (4-6): Demonstrable traction with early adopters or consistent growth metrics.
  - High (7-10): Strong traction with significant customer base, revenue, or rapid growth.

- **Financials**: Review the startup's financial health, runway, revenue generation, and fundraising success.
  - Low (1-3): Weak financials, short runway, or negligible revenue.
  - Moderate (4-6): Stable financials with some fundraising success but uncertain revenue streams.
  - High (7-10): Robust financial position, strong revenue, and sufficient funding.

- **Product Uniqueness**: Assess the innovation, differentiation, and problem-solving impact of the product or service.
  - Low (1-3): Generic product with little differentiation or problem-solving value.
  - Moderate (4-6): Some innovative features but overlaps with existing solutions.
  - High (7-10): Highly innovative, solving critical pain points with clear differentiation.

- **Competitive Landscape**: Evaluate the startup's position relative to competitors and barriers to entry.
  - Low (1-3): Highly competitive market with no clear advantage.
  - Moderate (4-6): Moderate competition with potential for differentiation.
  - High (7-10): Limited competition, strong differentiation, or high barriers to entry.

- **Business Model Clarity**: Analyze the clarity, scalability, and sustainability of the business model.
  - Low (1-3): Unclear or unsustainable business model with weak revenue streams.
  - Moderate (4-6): Clear but evolving model with moderate scalability.
  - High (7-10): Well-defined, scalable, and sustainable model with strong revenue potential.

- **Risk Factors**: Assess market, operational, financial, technological, regulatory, and scalability risks.
  - Low (1-3): High risks with minimal mitigation strategies.
  - Moderate (4-6): Moderate risks with some mitigation plans in place.
  - High (7-10): Low risks or robust mitigation strategies ensuring stability.

**Scoring Guidelines**:
- **Score**: Assign an integer (1-10) based on the startup's performance for each parameter, using the provided criteria.
- **Threshold**: Set an integer (1-10) representing the minimum score required to be competitive in the industry, based on industry standards and competition.
- **Benchmark_normalized**: Assign an integer (1-10) based on the performance of the top 3 competitors in the same category. For example, if top competitors have founders from elite institutions or serial entrepreneurs, set a high benchmark (7-10) for Team Quality and score the startup lower if it lacks similar credentials.

**Output Format**:
Return a valid JSON object structured as follows:

{
  "startup_score": [
    {
      "Parameter": "Team_Quality",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Market_Size",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Traction",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Financials",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Product_Uniqueness",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Competitive_Landscape",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Business_Model_Clarity",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    },
    {
      "Parameter": "Risk_Factors",
      "Score": <1-10>,
      "Threshold": <1-10>,
      "Benchmark_normalized": <1-10>
    }
  ]
}

"""