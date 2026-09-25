"""
Gemini Multimodal Vision Service for VisionCaption AI.
Deep visual understanding, zero-hallucination grounding,
and native multilingual explanation generation.
"""

import json
import logging
from typing import Dict, Any, Optional
from PIL import Image
import io

from app.config import settings
from app.languages import get_language

logger = logging.getLogger("visioncaption.gemini")

class VisionServiceError(Exception):
    """Custom exception for vision analysis failures."""
    pass

class NoAPIKeyError(VisionServiceError):
    """Raised when no Gemini API key is configured."""
    pass

ANALYSIS_SCHEMA_PROMPT = """
You are VisionCaption AI, an advanced, world-class multimodal image understanding system.
Analyze this image thoroughly and provide a structured, deeply informative visual breakdown.

CRITICAL INSTRUCTIONS:
1. TARGET LANGUAGE: ALL user-facing explanation strings MUST be generated purely and naturally in {language_name} ({language_native_name}). Do NOT output English unless the requested target language is English.
2. HONEST FACTUAL GROUNDING (NO HALLUCINATIONS): Ground every statement strictly on what is physically visible in the image.
   If any aspect (e.g. specific scene context, exact relationship, or identity) is ambiguous, occluded, or cannot be determined with certainty, explicitly state that it cannot be determined instead of inventing an answer.
3. PRIVACY & SAFETY: Do NOT identify real people by name or infer private/sensitive personal attributes. For people, provide only approximate counts, visible postures, clothing, or general visible activities.
4. SCENE / CONTEXT: Explain what type of scene it appears to be when reasonably identifiable (e.g. classroom, office, street, outdoor environment, event, food scene, nature, technology, document, etc.). Do not force the AI to select a category when the scene is unclear; explicitly state "Unclear / Ambiguous" if not identifiable.
5. READ ALOUD SCRIPT: Provide a cohesive, engaging spoken narrative in the target language designed to be read aloud via voice. It should seamlessly guide the listener through the caption, scene, and key highlights naturally.

You MUST respond with ONLY a valid JSON object matching this exact schema:
{
  "short_caption": "A concise and meaningful 1-2 sentence summary of what the image shows in the target language.",
  "detailed_description": "A comprehensive, natural 1-2 paragraph explanation covering the main subjects, notable objects, environment, actions taking place, and spatial relationships.",
  "scene_context": {
    "category": "Classification of the scene (e.g., Classroom, Office, Street, Nature, Event, Kitchen, Workshop, or 'Unclear / Ambiguous')",
    "is_ambiguous": false,
    "explanation": "Detailed explanation describing the setting, background, and physical context."
  },
  "important_elements": [
    {
      "name": "Object or subject name",
      "detail": "Description of its appearance, state, or position",
      "prominence": "primary"
    }
  ],
  "activities_actions": [
    "Description of visible actions, movements, or interactions (or 'No dynamic activity observed' if static)."
  ],
  "people_information": {
    "detected": true,
    "approximate_count": "e.g. '3 to 5 individuals' or '0 (No people detected)' or 'Crowd, exact count indeterminate'",
    "visible_roles_or_activities": "What people appear to be doing or wearing (based strictly on visual evidence).",
    "clarity_notes": "Any visual limitations like occlusion, distance, blur, etc."
  },
  "visual_insights": {
    "lighting_and_atmosphere": "Lighting source, natural vs artificial, time of day cues, atmosphere/mood.",
    "composition_and_colors": "Dominant colors, framing, perspective/angle, depth of field.",
    "notable_observations": [
      "Key subtle detail 1",
      "Key subtle detail 2"
    ]
  },
  "read_aloud_summary": "A smooth, cohesive spoken narrative script in the target language designed specifically to be read aloud via voice."
}
"""

QA_PROMPT = """
You are VisionCaption AI answering a user question about this specific image.
User's Question: "{question}"
Target Language: Answer fluently in {language_name} ({language_native_name}).

Guidelines:
- Answer accurately based ONLY on what is visible in the image.
- If the question asks about something not visible or cannot be determined, state honestly that it cannot be determined from the image.
- Provide a direct, helpful answer in 2-4 sentences.
"""

class GeminiVisionService:
    def __init__(self):
        self.default_api_key = settings.gemini_api_key
        self.preferred_models = [settings.primary_model, settings.fallback_model, "gemini-2.0-flash"]

    def _get_client(self, api_key: Optional[str] = None):
        """Initialize Google GenAI Client with the active API key."""
        active_key = api_key or self.default_api_key
        if not active_key or not active_key.strip():
            raise NoAPIKeyError(
                "Gemini API Key is required. Please provide a key in the settings modal or set GEMINI_API_KEY environment variable."
            )
        try:
            from google import genai
            return genai.Client(api_key=active_key.strip())
        except Exception as e:
            raise VisionServiceError(f"Failed to initialize Gemini client: {e}")

    def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """Validate if a provided Gemini API key is functional."""
        if not api_key or not api_key.strip():
            return {"valid": False, "message": "API Key cannot be empty."}
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            # Run a lightweight test generation
            response = client.models.generate_content(
                model=self.preferred_models[0],
                contents="Test ping. Respond with 'OK'."
            )
            return {
                "valid": True, 
                "message": "API Key validated successfully!",
                "model": self.preferred_models[0]
            }
        except Exception as e:
            error_str = str(e)
            if "API_KEY_INVALID" in error_str or "400" in error_str:
                return {"valid": False, "message": "Invalid API key. Please check and re-enter."}
            elif "QUOTA" in error_str.upper() or "429" in error_str:
                return {"valid": False, "message": "API key quota exceeded or rate limited."}
            return {"valid": False, "message": f"Validation failed: {error_str}"}

    def analyze_image(
        self, 
        image_bytes: bytes, 
        lang_code: str = "en", 
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform complete deep visual understanding analysis using Gemini.
        Returns validated structured JSON in the target language.
        """
        client = self._get_client(api_key)
        
        # Resolve language metadata
        lang_info = get_language(lang_code)
        lang_name = lang_info.name if lang_info else "English"
        lang_native = lang_info.native_name if lang_info else "English"

        prompt = ANALYSIS_SCHEMA_PROMPT.format(
            language_name=lang_name,
            language_native_name=lang_native
        )

        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            # Convert to RGB if palette or alpha
            if pil_image.mode not in ("RGB", "L"):
                pil_image = pil_image.convert("RGB")
        except Exception as e:
            raise VisionServiceError(f"Invalid or corrupted image format: {e}")

        # Attempt models in order
        last_error = None
        for model_name in self.preferred_models:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=model_name,
                    contents=[pil_image, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2, # low temperature for honest factual grounding
                    )
                )
                
                raw_text = response.text.strip()
                # Parse JSON
                result = json.loads(raw_text)
                
                # Enrich with language metadata
                result["language_code"] = lang_code
                result["language_name"] = lang_name
                result["language_native_name"] = lang_native
                result["model_used"] = model_name

                return result

            except Exception as e:
                logger.warning(f"Model {model_name} failed: {e}")
                last_error = e
                continue

        # If all models failed
        raise VisionServiceError(f"Image analysis failed with available models: {last_error}")

    def ask_image_question(
        self,
        image_bytes: bytes,
        question: str,
        lang_code: str = "en",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ask an interactive follow-up question about the image in the selected language."""
        client = self._get_client(api_key)
        
        lang_info = get_language(lang_code)
        lang_name = lang_info.name if lang_info else "English"
        lang_native = lang_info.native_name if lang_info else "English"

        prompt = QA_PROMPT.format(
            question=question.strip(),
            language_name=lang_name,
            language_native_name=lang_native
        )

        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            if pil_image.mode not in ("RGB", "L"):
                pil_image = pil_image.convert("RGB")
        except Exception as e:
            raise VisionServiceError(f"Invalid image format: {e}")

        for model_name in self.preferred_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[pil_image, prompt]
                )
                answer = response.text.strip()
                return {
                    "question": question,
                    "answer": answer,
                    "language_code": lang_code,
                    "model_used": model_name
                }
            except Exception as e:
                logger.warning(f"Q&A Model {model_name} failed: {e}")
                continue

        raise VisionServiceError("Unable to answer question with available models.")

gemini_service = GeminiVisionService()
