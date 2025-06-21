"""
Simple configuration for hackathon
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Basic settings for hackathon"""
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # CORS settings
    ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
    
    # SerpAPI for Google Flights
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    
    # Use real API if key is available, otherwise mock
    USE_MOCK_DATA = not bool(SERPAPI_KEY)


# Create settings instance
settings = Settings()
