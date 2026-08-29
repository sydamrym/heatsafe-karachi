import os
from dotenv import load_dotenv

load_dotenv()

FORTYGUARD_API_KEY = os.getenv("FORTYGUARD_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
FORTYGUARD_BASE_URL = "https://api.fortyguard.com"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
