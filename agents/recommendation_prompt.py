def build_investor_prompt(startup_score, sector_benchmark_score, red_flags, green_flags, category_scores=None):
    """
    Builds a textual prompt for the investor recommendation agent.
    """
    prompt = f"Startup Score: {startup_score}\n"
    prompt += f"Sector Benchmark Score: {sector_benchmark_score}\n"
    
    if red_flags:
        prompt += f"Red Flags: {', '.join(red_flags)}\n"
    if green_flags:
        prompt += f"Green Flags: {', '.join(green_flags)}\n"
    if category_scores:
        prompt += "Category Scores:\n"
        for cat, score in category_scores.items():
            prompt += f"  {cat}: {score}\n"
    
    prompt += "\nProvide clear, actionable recommendations for investors based on these metrics."
    return prompt
