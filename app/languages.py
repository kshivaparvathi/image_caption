"""
Supported Languages Registry for VisionCaption AI.
Contains genuinely supported languages verified across both
Gemini multimodal understanding and gTTS text-to-speech engine.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel

class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    flag: str
    bcp47: str
    is_featured: bool = False
    speech_supported: bool = True

SUPPORTED_LANGUAGES: Dict[str, LanguageInfo] = {
    # Core Requested Languages
    "en": LanguageInfo(code="en", name="English", native_name="English", flag="🇺🇸", bcp47="en-US", is_featured=True),
    "te": LanguageInfo(code="te", name="Telugu", native_name="తెలుగు", flag="🇮🇳", bcp47="te-IN", is_featured=True),
    "hi": LanguageInfo(code="hi", name="Hindi", native_name="हिन्दी", flag="🇮🇳", bcp47="hi-IN", is_featured=True),
    "ta": LanguageInfo(code="ta", name="Tamil", native_name="தமிழ்", flag="🇮🇳", bcp47="ta-IN", is_featured=True),
    "kn": LanguageInfo(code="kn", name="Kannada", native_name="ಕನ್ನಡ", flag="🇮🇳", bcp47="kn-IN", is_featured=True),
    "ml": LanguageInfo(code="ml", name="Malayalam", native_name="മലയാളം", flag="🇮🇳", bcp47="ml-IN", is_featured=True),
    "bn": LanguageInfo(code="bn", name="Bengali", native_name="বাংলা", flag="🇮🇳", bcp47="bn-IN", is_featured=True),
    "mr": LanguageInfo(code="mr", name="Marathi", native_name="मराठी", flag="🇮🇳", bcp47="mr-IN", is_featured=True),
    
    # Additional Top Global Languages
    "es": LanguageInfo(code="es", name="Spanish", native_name="Español", flag="🇪🇸", bcp47="es-ES", is_featured=True),
    "fr": LanguageInfo(code="fr", name="French", native_name="Français", flag="🇫🇷", bcp47="fr-FR", is_featured=True),
    "de": LanguageInfo(code="de", name="German", native_name="Deutsch", flag="🇩🇪", bcp47="de-DE", is_featured=True),
    "it": LanguageInfo(code="it", name="Italian", native_name="Italiano", flag="🇮🇹", bcp47="it-IT", is_featured=True),
    "pt": LanguageInfo(code="pt", name="Portuguese", native_name="Português", flag="🇧🇷", bcp47="pt-BR", is_featured=True),
    "gu": LanguageInfo(code="gu", name="Gujarati", native_name="ગુજરાતી", flag="🇮🇳", bcp47="gu-IN", is_featured=True),
    "ja": LanguageInfo(code="ja", name="Japanese", native_name="日本語", flag="🇯🇵", bcp47="ja-JP", is_featured=True),
    "ko": LanguageInfo(code="ko", name="Korean", native_name="한국어", flag="🇰🇷", bcp47="ko-KR", is_featured=True),
    "zh-CN": LanguageInfo(code="zh-CN", name="Chinese (Simplified)", native_name="简体中文", flag="🇨🇳", bcp47="zh-CN", is_featured=True),
    "zh-TW": LanguageInfo(code="zh-TW", name="Chinese (Traditional)", native_name="繁體中文", flag="🇹🇼", bcp47="zh-TW", is_featured=False),
    "ar": LanguageInfo(code="ar", name="Arabic", native_name="العربية", flag="🇸🇦", bcp47="ar-SA", is_featured=True),
    "ru": LanguageInfo(code="ru", name="Russian", native_name="Русский", flag="🇷🇺", bcp47="ru-RU", is_featured=True),
    "tr": LanguageInfo(code="tr", name="Turkish", native_name="Türkçe", flag="🇹🇷", bcp47="tr-TR", is_featured=True),
    
    # Additional Verified Supported Languages
    "af": LanguageInfo(code="af", name="Afrikaans", native_name="Afrikaans", flag="🇿🇦", bcp47="af-ZA"),
    "bg": LanguageInfo(code="bg", name="Bulgarian", native_name="Български", flag="🇧🇬", bcp47="bg-BG"),
    "bs": LanguageInfo(code="bs", name="Bosnian", native_name="Bosanski", flag="🇧🇦", bcp47="bs-BA"),
    "ca": LanguageInfo(code="ca", name="Catalan", native_name="Català", flag="🇪🇸", bcp47="ca-ES"),
    "cs": LanguageInfo(code="cs", name="Czech", native_name="Čeština", flag="🇨🇿", bcp47="cs-CZ"),
    "cy": LanguageInfo(code="cy", name="Welsh", native_name="Cymraeg", flag="🇬🇧", bcp47="cy-GB"),
    "da": LanguageInfo(code="da", name="Danish", native_name="Dansk", flag="🇩🇰", bcp47="da-DK"),
    "el": LanguageInfo(code="el", name="Greek", native_name="Ελληνικά", flag="🇬🇷", bcp47="el-GR"),
    "et": LanguageInfo(code="et", name="Estonian", native_name="Eesti", flag="🇪🇪", bcp47="et-EE"),
    "fi": LanguageInfo(code="fi", name="Finnish", native_name="Suomi", flag="🇫🇮", bcp47="fi-FI"),
    "hr": LanguageInfo(code="hr", name="Croatian", native_name="Hrvatski", flag="🇭🇷", bcp47="hr-HR"),
    "hu": LanguageInfo(code="hu", name="Hungarian", native_name="Magyar", flag="🇭🇺", bcp47="hu-HU"),
    "hy": LanguageInfo(code="hy", name="Armenian", native_name="Հայերեն", flag="🇦🇲", bcp47="hy-AM"),
    "id": LanguageInfo(code="id", name="Indonesian", native_name="Bahasa Indonesia", flag="🇮🇩", bcp47="id-ID"),
    "is": LanguageInfo(code="is", name="Icelandic", native_name="Íslenska", flag="🇮🇸", bcp47="is-IS"),
    "iw": LanguageInfo(code="iw", name="Hebrew", native_name="עברית", flag="🇮🇱", bcp47="he-IL"),
    "km": LanguageInfo(code="km", name="Khmer", native_name="ភាសាខ្មែរ", flag="🇰🇭", bcp47="km-KH"),
    "lv": LanguageInfo(code="lv", name="Latvian", native_name="Latviešu", flag="🇱🇻", bcp47="lv-LV"),
    "mk": LanguageInfo(code="mk", name="Macedonian", native_name="Македонски", flag="🇲🇰", bcp47="mk-MK"),
    "ms": LanguageInfo(code="ms", name="Malay", native_name="Bahasa Melayu", flag="🇲🇾", bcp47="ms-MY"),
    "my": LanguageInfo(code="my", name="Burmese", native_name="မြန်မာစာ", flag="🇲🇲", bcp47="my-MM"),
    "ne": LanguageInfo(code="ne", name="Nepali", native_name="नेपाली", flag="🇳🇵", bcp47="ne-NP"),
    "nl": LanguageInfo(code="nl", name="Dutch", native_name="Nederlands", flag="🇳🇱", bcp47="nl-NL"),
    "no": LanguageInfo(code="no", name="Norwegian", native_name="Norsk", flag="🇳🇴", bcp47="no-NO"),
    "pl": LanguageInfo(code="pl", name="Polish", native_name="Polski", flag="🇵🇱", bcp47="pl-PL"),
    "ro": LanguageInfo(code="ro", name="Romanian", native_name="Română", flag="🇷🇴", bcp47="ro-RO"),
    "si": LanguageInfo(code="si", name="Sinhala", native_name="සිංහල", flag="🇱🇰", bcp47="si-LK"),
    "sk": LanguageInfo(code="sk", name="Slovak", native_name="Slovenčina", flag="🇸🇰", bcp47="sk-SK"),
    "sq": LanguageInfo(code="sq", name="Albanian", native_name="Shqip", flag="🇦🇱", bcp47="sq-AL"),
    "sr": LanguageInfo(code="sr", name="Serbian", native_name="Српски", flag="🇷🇸", bcp47="sr-RS"),
    "su": LanguageInfo(code="su", name="Sundanese", native_name="Basa Sunda", flag="🇮🇩", bcp47="su-ID"),
    "sv": LanguageInfo(code="sv", name="Swedish", native_name="Svenska", flag="🇸🇪", bcp47="sv-SE"),
    "sw": LanguageInfo(code="sw", name="Swahili", native_name="Kiswahili", flag="🇰🇪", bcp47="sw-KE"),
    "th": LanguageInfo(code="th", name="Thai", native_name="ไทย", flag="🇹🇭", bcp47="th-TH"),
    "tl": LanguageInfo(code="tl", name="Filipino", native_name="Tagalog", flag="🇵🇭", bcp47="tl-PH"),
    "uk": LanguageInfo(code="uk", name="Ukrainian", native_name="Українська", flag="🇺🇦", bcp47="uk-UA"),
    "ur": LanguageInfo(code="ur", name="Urdu", native_name="اردو", flag="🇵🇰", bcp47="ur-PK"),
    "vi": LanguageInfo(code="vi", name="Vietnamese", native_name="Tiếng Việt", flag="🇻🇳", bcp47="vi-VN"),
}

def get_all_languages() -> List[LanguageInfo]:
    """Return all supported languages: featured first, then sorted alphabetically."""
    featured = [lang for lang in SUPPORTED_LANGUAGES.values() if lang.is_featured]
    others = [lang for lang in SUPPORTED_LANGUAGES.values() if not lang.is_featured]
    others_sorted = sorted(others, key=lambda x: x.name)
    return featured + others_sorted

def get_language(code: str) -> Optional[LanguageInfo]:
    """Retrieve language metadata by code."""
    if not code:
        return None
    code_norm = code.strip()
    if code_norm in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[code_norm]
    # Check lowercase or prefix fallback (e.g. 'en-US' -> 'en')
    for k, v in SUPPORTED_LANGUAGES.items():
        if k.lower() == code_norm.lower() or k.lower() == code_norm.split('-')[0].lower():
            return v
    return None

def is_supported(code: str) -> bool:
    """Validate whether language code is genuinely supported."""
    return get_language(code) is not None

def get_featured_languages() -> List[LanguageInfo]:
    """Return featured quick-access languages."""
    return [lang for lang in SUPPORTED_LANGUAGES.values() if lang.is_featured]
