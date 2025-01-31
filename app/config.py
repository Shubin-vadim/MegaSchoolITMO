import os

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_SEARCH_KEY: str = os.getenv("GOOGLE_SEARCH_KEY", "")
    GOOGLE_SEARCH_CX: str = os.getenv("GOOGLE_SEARCH_CX", "")
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    CACHE_TTL: int = 3600
    
    MODEL_NAME: str = "gpt-4o-mini"
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.01
    
    REQUEST_TIMEOUT: int = 30

settings = Settings()
