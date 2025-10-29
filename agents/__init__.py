"""
ADK Agents Package
Startup Analyzer Agent Framework
"""
import os, sys
print(">>> INIT DEBUG:")
print(">>> __file__:", __file__)
print(">>> cwd:", os.getcwd())
print(">>> sys.path:", sys.path)
print(">>> contents of agents folder:", os.listdir(os.path.dirname(__file__)))

# from .root_agent import StartupAnalyzerAgent
from agents.root_agent import StartupAnalyzerAgent


# try:
#     from .root_agent import StartupAnalyzerAgent
# except ImportError:
#     # fallback if Streamlit changes package context
#     import importlib.util, os, sys
#     module_path = os.path.join(os.path.dirname(__file__), "root_agent.py")
#     spec = importlib.util.spec_from_file_location("root_agent", module_path)
#     root_agent = importlib.util.module_from_spec(spec)
#     sys.modules["root_agent"] = root_agent
#     spec.loader.exec_module(root_agent)
#     StartupAnalyzerAgent = root_agent.StartupAnalyzerAgent

from .data_processing_agent import DataProcessingAgent
from .calculation_agent import CalculationAgent

__all__ = [
    'StartupAnalyzerAgent',
    'DataProcessingAgent', 
    'CalculationAgent'
]
