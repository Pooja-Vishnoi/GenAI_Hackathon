"""
Vercel Serverless Function Entry Point
This file is required by Vercel for Python deployments
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app
from api_server import app

# Export handler for Vercel
handler = app
