import os
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# Try to load .env
env_file = Path('.env')
if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=True)
    print("Loaded .env from", env_file.absolute())

class Config:
    # DIRECT API KEY
    GEMINI_API_KEY: Optional[str] = "AIzaSyD1hj0AuW_0daGc91L7C8AP6_1R56z6fjA"
    LLM_PROVIDER: str = "gemini"
    
    # Firebase settings
    FIREBASE_DATABASE_URL: Optional[str] = os.getenv("FIREBASE_DATABASE_URL", "https://smart-cane-ai-default-rtdb.asia-southeast1.firebasedatabase.app/")
    FIREBASE_DATABASE_SECRET: Optional[str] = os.getenv("FIREBASE_DATABASE_SECRET", "zrmDiimzcJkIoHwfQN8KEXZWUBxhO9S8Llv3tD9v")
    
    # Alert thresholds
    ALERT_THRESHOLD_DISTANCE: float = float(os.getenv("ALERT_THRESHOLD_DISTANCE", "1.5"))
    CRITICAL_DISTANCE: float = float(os.getenv("CRITICAL_DISTANCE", "0.5"))
    FALL_THRESHOLD: float = float(os.getenv("FALL_THRESHOLD", "2.0"))
    
    AGENT_NAME: str = "SmartCaneAI"
    AGENT_VERSION: str = "1.0.0"
    
    @classmethod
    def print_status(cls):
        print("\n=== Configuration Status ===")
        print("Gemini API Key: SET")
        print("Firebase URL: SET")
        print("Firebase Secret: SET")
        print("LLM Provider:", cls.LLM_PROVIDER)
        print("============================\n")

config = Config()