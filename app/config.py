"""
Configuration and Environment Settings for Image Caption AI.
100% Open-source AI stack powered by Salesforce BLIP.
No external Gemini or third-party Vision API dependencies.
"""

import os
from pathlib import Path
from pydantic import BaseModel
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    app_name: str = "Image Caption AI"
    app_version: str = "2.1.0"
    app_description: str = "Turn your images into meaningful captions with open-source AI"
    
    # Upload limits & formats (JPG, JPEG, PNG, WEBP)
    max_upload_size_mb: int = 15
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Cache directory
    tts_cache_dir: Path = BASE_DIR / "cache" / "tts"
    
    # Host & Port
    host: str = os.environ.get("HOST", "0.0.0.0")
    port: int = int(os.environ.get("PORT", 8000))

settings = Settings()
settings.tts_cache_dir.mkdir(parents=True, exist_ok=True)
