"""
JobAssist - Agent IA d'adaptation de CV
"""

__version__ = "1.0.0"
__author__ = "JobAssist Team"

from .adapter import CVAdapter
from .config import load_api_keys

__all__ = ['CVAdapter', 'load_api_keys']
