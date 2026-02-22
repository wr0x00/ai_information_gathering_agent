"""
AI Information Gathering Agent
============================

An advanced AI-powered information gathering tool for cybersecurity professionals.
"""
__version__ = "1.0.0"
__author__ = "AI Security Research Team"

# Import main components for easy access
from .agent import InformationGatheringAgent as Agent
from .config import Settings as Config
from .storage import ResultsStorage as Storage
from .http_client import AsyncHTTPClient as HttpClient

# Import modules
from . import modules

# Define what gets imported with "from ai_agent import *"
__all__ = [
    "Agent",
    "Config",
    "Storage",
    "HttpClient",
    "modules"
]
