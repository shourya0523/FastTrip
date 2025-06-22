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
    
    # Use mock data setting from environment, with fallback logic
    USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true" or not bool(SERPAPI_KEY)