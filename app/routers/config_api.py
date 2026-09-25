"""
Configuration and Metadata Router for Image Caption AI.
Provides endpoints for platforms metadata, supported languages,
health check, and benchmark sample scenes.
100% open-source, no external API keys required.
"""

from fastapi import APIRouter
from typing import List, Dict, Any

from app.config import settings
from app.languages import get_all_languages, get_featured_languages
from app.services.platform_caption_service import PLATFORMS_CONFIG
from app.services.sample_data import SAMPLE_DATA

router = APIRouter(prefix="/api", tags=["Configuration & Metadata"])

@router.get("/platforms")
async def list_platforms():
    """Return all supported platform profiles with metadata and prompt guidelines."""
    return {
        "platforms": list(PLATFORMS_CONFIG.values())
    }

@router.get("/languages")
async def list_languages():
    """Return all genuinely supported languages and featured quick-access items."""
    return {
        "total": len(get_all_languages()),
        "featured": [l.model_dump() for l in get_featured_languages()],
        "languages": [l.model_dump() for l in get_all_languages()]
    }

@router.get("/samples")
async def list_samples():
    """Return benchmark sample scenes available for quick one-click evaluation."""
    samples = []
    for k, v in SAMPLE_DATA.items():
        samples.append({
            "id": v.id,
            "title": v.title,
            "category": v.category,
            "description": v.description,
            "filename": v.filename,
            "image_url": f"/static/samples/{v.filename}",
            "dominant_color": v.dominant_color
        })
    return {"samples": samples}

@router.get("/health")
async def health_check():
    """System health check and engine status."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "ai_engine": "Salesforce BLIP + BLIP VQA (On-Device Open Source)",
        "external_api_keys": False,
        "supported_platforms": list(PLATFORMS_CONFIG.keys()),
        "supported_languages_count": len(get_all_languages()),
        "max_upload_size_mb": settings.max_upload_size_mb
    }
