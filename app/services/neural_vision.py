"""
Neural Vision Engine for VisionCaption AI.
Performs genuine on-device deep learning visual understanding using
Salesforce BLIP models cached locally. Accurately identifies subjects,
objects, context, and actions without any API key dependencies.
"""

import sys
import logging
from typing import Dict, Any, Optional, List
from PIL import Image
import io
import urllib.request
import urllib.parse
import json

from app.languages import get_language

logger = logging.getLogger("visioncaption.neural")

_blip_processor = None
_blip_model = None
_vqa_processor = None
_vqa_model = None

def get_blip_caption_model():
    global _blip_processor, _blip_model
    if _blip_model is None:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration
        logger.info("Initializing BLIP Captioning Model from local cache...")
        for model_id in ["Salesforce/blip-image-captioning-large", "Salesforce/blip-image-captioning-base"]:
            try:
                _blip_processor = BlipProcessor.from_pretrained(model_id, local_files_only=True)
                _blip_model = BlipForConditionalGeneration.from_pretrained(model_id, local_files_only=True)
                _blip_model.eval()
                logger.info(f"Loaded BLIP model: {model_id}")
                break
            except Exception as e:
                logger.warning(f"Could not load {model_id}: {e}")
                continue
    return _blip_processor, _blip_model

def get_blip_vqa_model():
    global _vqa_processor, _vqa_model
    if _vqa_model is None:
        import torch
        from transformers import BlipProcessor, BlipForQuestionAnswering
        logger.info("Initializing BLIP VQA Model from local cache...")
        try:
            _vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base", local_files_only=True)
            _vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base", local_files_only=True)
            _vqa_model.eval()
            logger.info("Loaded BLIP VQA model successfully")
        except Exception as e:
            logger.warning(f"Could not load BLIP VQA model: {e}")
    return _vqa_processor, _vqa_model

def translate_text(text: str, target_lang: str) -> str:
    """Translate text to the target language if not English."""
    if not text or target_lang in ("en", "en-US"):
        return text
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode("utf-8"))
        return "".join([part[0] for part in data[0] if part[0]])
    except Exception as e:
        logger.warning(f"Translation failed for {target_lang}: {e}")
        return text

class NeuralVisionService:
    """End-to-end true visual understanding service."""

    def analyze(self, image_bytes: bytes, target_lang: str = "en") -> Dict[str, Any]:
        import torch

        try:
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != "RGB":
                image = image.convert("RGB")
        except Exception as e:
            raise ValueError(f"Unable to read image: {e}")

        # 1. Generate core caption using BLIP
        processor, model = get_blip_caption_model()
        if model is None:
            raise RuntimeError("Neural vision model could not be initialized.")

        inputs = processor(image, return_tensors="pt")
        with torch.no_grad():
            output_tokens = model.generate(**inputs, max_new_tokens=60, num_beams=3)
        raw_caption = processor.decode(output_tokens[0], skip_special_tokens=True).strip()
        
        # Clean prefix artifacts like "there is a picture of..."
        clean_raw = raw_caption
        prefixes = ["there is a picture of ", "there are ", "a photograph of ", "an image of ", "a close up of "]
        for p in prefixes:
            if clean_raw.lower().startswith(p):
                clean_raw = clean_raw[len(p):]
                break

        if clean_raw:
            clean_caption = clean_raw[0].upper() + clean_raw[1:]
            if not clean_caption.endswith("."):
                clean_caption += "."
        else:
            clean_caption = "Visible visual scene with identifiable subjects."

        # 2. Extract structured visual dimensions using BLIP VQA
        vqa_proc, vqa_mod = get_blip_vqa_model()
        vqa_answers = {}

        if vqa_mod is not None:
            questions = {
                "setting": "is this indoor or outdoor?",
                "scene": "where is this scene taking place?",
                "objects": "what are the main objects?",
                "people_count": "how many people are visible?"
            }

            for key, q in questions.items():
                try:
                    q_inputs = vqa_proc(image, q, return_tensors="pt")
                    with torch.no_grad():
                        out = vqa_mod.generate(**q_inputs, max_new_tokens=25)
                    ans = vqa_proc.decode(out[0], skip_special_tokens=True).strip()
                    vqa_answers[key] = ans
                except Exception:
                    vqa_answers[key] = ""

        # 3. Assemble natural sections
        scene_answer = vqa_answers.get("scene", "").strip().lower()
        setting_answer = vqa_answers.get("setting", "").strip().lower()
        objects_answer = vqa_answers.get("objects", "").strip().lower()
        people_count = vqa_answers.get("people_count", "").strip().lower()

        # Build natural "What I see" explanation
        what_i_see_parts = [clean_caption]
        if objects_answer and objects_answer not in ("nothing", "none", "unknown", "") and objects_answer not in clean_raw.lower():
            what_i_see_parts.append(f"Main visible items include {objects_answer}.")
        what_i_see = " ".join(what_i_see_parts)

        # Build Scene section (Only if genuinely identifiable)
        scene_text = None
        if scene_answer and scene_answer not in ("unknown", "unclear", "none", "no", "yes"):
            clean_scene = scene_answer.replace("in ", "").replace("at ", "")
            if setting_answer in ("indoor", "outdoor") and setting_answer not in clean_scene:
                scene_text = f"{setting_answer.capitalize()} environment in a {clean_scene}."
            else:
                scene_text = f"Setting: {clean_scene.capitalize()} environment."
        elif setting_answer in ("indoor", "outdoor"):
            scene_text = f"{setting_answer.capitalize()} environment."

        # Build Key Details (Relevant factual elements)
        key_details = []
        if objects_answer and objects_answer not in ("none", "nothing", ""):
            key_details.append(f"Notable elements: {objects_answer.capitalize()}")
        if setting_answer in ("indoor", "outdoor"):
            key_details.append(f"Environment: {setting_answer.capitalize()}")
        
        w, h = image.size
        framing = "Wide landscape composition" if w > h * 1.3 else ("Portrait composition" if h > w * 1.3 else "Balanced framing")
        key_details.append(f"Framing: {framing}")

        # Build Activity (ONLY if there are living subjects)
        has_people = people_count not in ("0", "no", "none", "no one", "nobody", "zero", "") and any(w in raw_caption.lower() for w in ["people", "person", "man", "woman", "standing", "sitting", "walking"])
        has_animal = any(w in raw_caption.lower() for w in ["dog", "cat", "bird", "horse", "animal"])

        activity_text = None
        if (has_people or has_animal) and vqa_mod is not None:
            try:
                act_inputs = vqa_proc(image, "what are they doing?", return_tensors="pt")
                with torch.no_grad():
                    act_out = vqa_mod.generate(**act_inputs, max_new_tokens=25)
                act_ans = vqa_proc.decode(act_out[0], skip_special_tokens=True).strip()
                if act_ans and act_ans not in ("nothing", "none", "unknown", "no"):
                    activity_text = f"Observed activity: {act_ans.capitalize()}."
            except Exception:
                pass

        # 4. Multilingual Translation
        lang_info = get_language(target_lang)
        lang_name = lang_info.name if lang_info else "English"
        lang_native = lang_info.native_name if lang_info else "English"

        translated_caption = translate_text(clean_caption, target_lang)
        translated_what_i_see = translate_text(what_i_see, target_lang)
        translated_scene = translate_text(scene_text, target_lang) if scene_text else None
        translated_activity = translate_text(activity_text, target_lang) if activity_text else None
        translated_key_details = [translate_text(item, target_lang) for item in key_details] if key_details else []

        # Cohesive full speech narrative in target language
        speech_parts = [translated_caption]
        if translated_scene:
            speech_parts.append(translated_scene)
        if translated_activity:
            speech_parts.append(translated_activity)
        full_speech_text = " ".join(speech_parts)

        return {
            "caption": translated_caption,
            "what_i_see": translated_what_i_see,
            "scene": translated_scene,
            "key_details": translated_key_details,
            "activity": translated_activity,
            "full_speech": full_speech_text,
            "language_code": target_lang,
            "language_name": lang_name,
            "language_native_name": lang_native,
            "raw_english_caption": clean_caption
        }

neural_vision_service = NeuralVisionService()
