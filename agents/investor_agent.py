import os
from dotenv import load_dotenv
from google.adk.agents import Agent  # Only if you are using ADK Agents
from google import genai
from google.genai import types
from .recommendation_prompt import build_investor_prompt

# Load API key
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")

# Initialize GenAI client
client = genai.Client(api_key=api_key)
GEMINI_MODEL = "gemini-2.0-flash"


def investor_recommendation_executor(startup_score: int,
                                     sector_benchmark_score: int,
                                     red_flags: list,
                                     green_flags: list,
                                     category_scores: dict = None, 
                                     temperature:float=0.7,
                                     max_output_tokens: int = 500) -> str:
    """
    Generates investor recommendations using Google Gemini.
    """
    
    prompt = build_investor_prompt(startup_score, sector_benchmark_score, red_flags, green_flags, category_scores)
    print("Prompt:\n", prompt)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[{"text": prompt}],
        config=types.GenerateContentConfig(
        temperature= temperature,
        max_output_tokens= max_output_tokens
        ),
    )
    # print("Response:\n", response.candidates[0])

    final_text = "\n".join([part.text for part in response.candidates[0].content.parts])
    return final_text.strip()


investor_recommendation_agent = Agent(
    name="investor_recommendation_agent",
    description="Generates investor recommendations using startup metrics, flags, and benchmarks."
)
