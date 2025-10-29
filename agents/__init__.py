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

from .root_agent import StartupAnalyzerAgent
from .data_processing_agent import DataProcessingAgent
from .calculation_agent import CalculationAgent

__all__ = [
    'StartupAnalyzerAgent',
    'DataProcessingAgent', 
    'CalculationAgent'
]
