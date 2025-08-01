import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Depth Estimation API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "https://vercel.app"
    ]
    
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./models")
    TEMP_DIR: str = os.getenv("TEMP_DIR", "./temp")
    
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    DEFAULT_DEPTH_MODEL: str = "Intel/dpt-hybrid-midas"
    AVAILABLE_MODELS: List[str] = [
        "Intel/dpt-large",
        "Intel/dpt-hybrid-midas", 
        "LiheYoung/depth-anything-large-hf"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()