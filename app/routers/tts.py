"""
Text-to-Speech Streaming Router for VisionCaption AI.
Serves high-quality audio streams in the user's selected language.
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import urllib.parse

from app.services.tts_service import tts_service
from app.languages import is_supported, get_language

router = APIRouter(prefix="/api/tts", tags=["Voice & Speech"])

class PrepareAudioRequest(BaseModel):
    items: Dict[str, str] # e.g. {"caption": "...", "description": "..."}
    language: str

@router.get("")
async def stream_tts(
    text: str = Query(..., description="Text content to speak in target language"),
    lang: str = Query("en", description="Language code")
):
    """Generate and stream audio MP3 corresponding to the target language."""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    try:
        file_path, _ = tts_service.get_audio_path(text, lang)
        
        # Return file response with audio streaming headers
        return FileResponse(
            path=str(file_path),
            media_type="audio/mpeg",
            filename="visioncaption_voice.mp3",
            headers={
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=86400"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis error: {e}")

@router.post("/prepare")
async def prepare_audio_urls(req: PrepareAudioRequest):
    """Pre-compute audio cache for multiple sections and return direct playable URLs."""
    result = {}
    for key, text in req.items.items():
        if text and text.strip():
            try:
                # Pre-generate in cache
                tts_service.get_audio_path(text, req.language)
                encoded_text = urllib.parse.quote(text)
                result[key] = f"/api/tts?text={encoded_text}&lang={req.language}"
            except Exception:
                result[key] = None
        else:
            result[key] = None
    return {"audio_urls": result, "language": req.language}
