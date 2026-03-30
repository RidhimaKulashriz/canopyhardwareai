import os
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# Force load .env from current directory
env_file = Path('.env')
if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=True)
    print(f"✓ Loaded .env from {env_file.absolute()}")
else:
    print(f"✗ .env file not found at {env_file.absolute()}")

class Config:
    # Directly read from environment
    GEMINI_API_KEY: Optional[str] = os.environ.get("GEMINI_API_KEY", "")
    LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "mock")
    
    # Firebase settings
    FIREBASE_DATABASE_URL: Optional[str] = os.environ.get("FIREBASE_DATABASE_URL", "")
    FIREBASE_DATABASE_SECRET: Optional[str] = os.environ.get("FIREBASE_DATABASE_SECRET", "")
    
    # Alert thresholds
    ALERT_THRESHOLD_DISTANCE: float = float(os.environ.get("ALERT_THRESHOLD_DISTANCE", "1.5"))
    CRITICAL_DISTANCE: float = float(os.environ.get("CRITICAL_DISTANCE", "0.5"))
    FALL_THRESHOLD: float = float(os.environ.get("FALL_THRESHOLD", "2.0"))
    
    AGENT_NAME: str = "SmartCaneAI"
    AGENT_VERSION: str = "1.0.0"
    
    @classmethod
    def print_status(cls):
        """Print configuration status"""
        print("\n=== Configuration Status ===")
        print(f"Gemini API Key: {'✓ Set (' + cls.GEMINI_API_KEY[:15] + '...)' if cls.GEMINI_API_KEY else '✗ Missing'}")
        print(f"Firebase URL: {'✓ Set' if cls.FIREBASE_DATABASE_URL else '✗ Missing'}")
        print(f"Firebase Secret: {'✓ Set' if cls.FIREBASE_DATABASE_SECRET else '✗ Missing'}")
        print(f"LLM Provider: {cls.LLM_PROVIDER}")
        print("============================\n")

config = Config()
