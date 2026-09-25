"""
High-Performance Text-to-Speech Service for VisionCaption AI.
Integrates Google Text-to-Speech (gTTS) with local disk caching
and chunked audio streaming for natural multilingual voice.
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Optional, Tuple
from gtts import gTTS
from app.config import settings
from app.languages import get_language, is_supported

def clean_text_for_speech(text: str) -> str:
    """Sanitize text removing markdown, formatting, emojis and symbols for clear pronunciation."""
    if not text:
        return ""
    # Remove markdown links
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown headers, bold, italics, code blocks
    t = re.sub(r'[`#*_~]', '', t)
    # Remove bullet symbols and numbering prefixes at line starts
    t = re.sub(r'^\s*[-*•\d\.]+\s+', '', t, flags=re.MULTILINE)
    # Normalize multiple whitespace and newlines
    t = re.sub(r'\s+', ' ', t).strip()
    return t

class TTSService:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or settings.tts_cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Mapping for language codes that need mapping for gTTS
        self.code_mapping = {
            "zh": "zh-CN",
            "zh-TW": "zh-TW",
            "iw": "iw",  # Hebrew
        }

    def _resolve_gtts_lang(self, lang_code: str) -> str:
        """Resolve incoming language code to valid gTTS code."""
        code = lang_code.strip()
        if code in self.code_mapping:
            return self.code_mapping[code]
        # Check standard languages
        lang_info = get_language(code)
        if lang_info:
            return lang_info.code
        return "en"

    def get_audio_path(self, text: str, lang_code: str) -> Tuple[Path, str]:
        """
        Generate or retrieve cached MP3 file path for given text and language.
        Returns (filepath, cleaned_text).
        """
        clean_text = clean_text_for_speech(text)
        if not clean_text:
            clean_text = "No content available to read aloud."

        resolved_lang = self._resolve_gtts_lang(lang_code)
        
        # Unique cache key
        cache_key = hashlib.sha256(f"{resolved_lang}::{clean_text}".encode("utf-8")).hexdigest()
        file_path = self.cache_dir / f"{cache_key}.mp3"

        if not file_path.exists():
            try:
                tts = gTTS(text=clean_text, lang=resolved_lang, slow=False)
                tts.save(str(file_path))
            except Exception as e:
                # If specific language fails, attempt English fallback
                if resolved_lang != "en":
                    tts = gTTS(text=clean_text, lang="en", slow=False)
                    tts.save(str(file_path))
                else:
                    raise RuntimeError(f"Text-to-speech generation failed: {e}")

        return file_path, clean_text

    def stream_audio(self, file_path: Path, chunk_size: int = 64 * 1024):
        """Yield chunks of audio data for streaming."""
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

tts_service = TTSService()
