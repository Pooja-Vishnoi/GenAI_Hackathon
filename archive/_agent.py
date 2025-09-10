# https://github.com/GoogleCloudPlatform/devrel-demos/blob/main/ai-ml/agent-patterns/1-llm-single-agent/agent.py
#   Single agent with tools

import os
from dotenv import load_dotenv  
import google.generativeai as genai
from google.adk.agents import Agent
from google.genai import types

from .tools.tools import get_purchase_history, check_refund_eligibility, process_refund
from .tools.prompts import top_level_prompt  

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env")) 
  
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:  
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")
genai.configure(api_key=api_key)

GEMINI_MODEL = "gemini-2.0-flash"
  
root_agent = Agent(  
    model=GEMINI_MODEL, 
    name="RefundSingleAgent",
    description="Customer refund single-agent for Crabby's Taffy company",
    instruction=top_level_prompt,
    tools=[get_purchase_history, check_refund_eligibility, process_refund],
)
