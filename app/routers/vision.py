"""
Vision and Platform Caption Router for Image Caption AI.
Processes image uploads or sample scenes, executes open-source BLIP vision analysis,
and returns platform-tailored, multilingual captions with optional text/voice instructions.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional, Dict, Any
from pathlib import Path
from PIL import Image
import io
import logging

from app.config import settings
from app.languages import is_supported
from app.services.platform_caption_service import platform_caption_service, PLATFORMS_CONFIG
from app.services.sample_data import SAMPLE_DATA

logger = logging.getLogger("imagecaption.router")
router = APIRouter(prefix="/api", tags=["Caption Generation"])

async def extract_image_bytes(file: Optional[UploadFile], sample_id: Optional[str]) -> bytes:
    """Validate and read image bytes from file upload or sample scene."""
    image_bytes = None

    if sample_id and sample_id in SAMPLE_DATA and not file:
        sample_info = SAMPLE_DATA[sample_id]
        sample_path = Path("static/samples") / sample_info.filename
        if sample_path.exists():
            with open(sample_path, "rb") as f:
                image_bytes = f.read()

    elif file:
        filename = file.filename or "upload.jpg"
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported format '.{ext}'. Supported formats: {', '.join(settings.allowed_extensions).upper()}"
            )

        image_bytes = await file.read()
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty. Please select a valid image file."
            )

        max_bytes = settings.max_upload_size_mb * 1024 * 1024
        if len(image_bytes) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image file exceeds maximum allowed limit of {settings.max_upload_size_mb} MB."
            )

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image uploaded. Please upload an image or choose a sample to continue."
        )

    # Validate image readability with PIL
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is corrupted or not a valid image."
        )

    return image_bytes

@router.post("/generate")
async def generate_platform_caption(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    platform: str = Form("caption"),
    language: str = Form("en"),
    instruction: Optional[str] = Form(None),
    variation: int = Form(0)
):
    """
    Generate platform-adapted, multilingual image caption using open-source BLIP AI.
    Supports Instagram, X/Twitter, LinkedIn, Facebook, WhatsApp, and General Caption.
    """
    if not is_supported(language):
        language = "en"
    if platform not in PLATFORMS_CONFIG:
        platform = "caption"

    actual_file = file or image
    image_bytes = await extract_image_bytes(actual_file, sample_id)

    try:
        result = platform_caption_service.generate(
            image_bytes=image_bytes,
            platform=platform,
            target_lang=language,
            user_instruction=instruction,
            variation=variation
        )
        return result

    except Exception as e:
        logger.error(f"Platform caption generation failed: {e}", exc_info=True)
        error_detail = str(e) if "Unable to analyze" in str(e) else "Unable to analyze this image. Please try again."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail
        )

@router.post("/analyze")
async def legacy_analyze_image(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    language: str = Form("en"),
    platform: Optional[str] = Form("caption")
):
    """
    Backwards-compatible analysis endpoint supporting legacy callers.
    """
    if not is_supported(language):
        language = "en"
    actual_file = file or image
    image_bytes = await extract_image_bytes(actual_file, sample_id)

    try:
        res = platform_caption_service.generate(
            image_bytes=image_bytes,
            platform=platform or "caption",
            target_lang=language
        )
        # Adapt format for legacy test assertions
        return {
            "caption": res["caption"],
            "what_i_see": res["visual_analysis"].get("raw_description", ""),
            "scene": res["visual_analysis"].get("category", "General Scene"),
            "language_code": res["language"]["code"],
            "language_name": res["language"]["name"],
            "audio_urls": {
                "caption": res["audio_url"],
                "full": res["audio_url"]
            },
            "visual_analysis": res["visual_analysis"],
            "platform": res["platform"]
        }
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze image."
        )
