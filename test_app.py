"""
Comprehensive Test Suite for Image Caption AI.
Verifies all platform routes, API endpoints, BLIP image understanding,
multilingual translations (Telugu, Hindi, etc.), instruction handling,
TTS streaming, and platform-specific format adaptations.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import unittest
from fastapi.testclient import TestClient
from main import app

class ImageCaptionAITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        with open("static/samples/nature_wildlife.jpg", "rb") as f:
            cls.mountains_img = f.read()
        with open("static/samples/tech_collaboration.jpg", "rb") as f:
            cls.tech_img = f.read()

    def test_01_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app_name"], "Image Caption AI")
        self.assertFalse(data["external_api_keys"])
        self.assertIn("Salesforce BLIP", data["ai_engine"])
        print("[PASS] Health check verified: 100% open-source BLIP stack")

    def test_02_platforms_metadata(self):
        res = self.client.get("/api/platforms")
        self.assertEqual(res.status_code, 200)
        platforms = res.json()["platforms"]
        platform_ids = [p["id"] for p in platforms]
        required = ["instagram", "twitter", "linkedin", "facebook", "whatsapp", "caption"]
        for r in required:
            self.assertIn(r, platform_ids)
        print(f"[PASS] All 6 required platforms verified: {', '.join(platform_ids)}")

    def test_03_languages_registry(self):
        res = self.client.get("/api/languages")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["total"], 20)
        codes = [l["code"] for l in data["languages"]]
        for lang_code in ["en", "te", "hi", "ta", "kn", "ml", "bn", "mr"]:
            self.assertIn(lang_code, codes)
        print("[PASS] All required Indian & global languages present in registry")

    def test_04_routes_spa_serving(self):
        routes = ["/", "/instagram", "/twitter", "/linkedin", "/facebook", "/whatsapp", "/caption"]
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed")
            self.assertIn("Image Caption AI", res.text)
            self.assertIn("Turn your images into meaningful captions.", res.text)
            self.assertIn("Choose what you want to create", res.text)
        print(f"[PASS] All {len(routes)} frontend SPA routes return index.html correctly")

    def test_05_generate_instagram(self):
        res = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "instagram", "language": "en"}
        )
        self.assertEqual(res.status_code, 200)
        d = res.json()
        self.assertEqual(d["platform"]["id"], "instagram")
        self.assertTrue(len(d["hashtags"]) > 0)
        self.assertTrue(all(h.startswith("#") for h in d["hashtags"]))
        self.assertTrue(len(d["caption"]) > 10)
        self.assertIn("main_caption", d)
        self.assertIn("alternatives", d)
        self.assertEqual(len(d["alternatives"]), 4)
        for alt in d["alternatives"]:
            self.assertTrue(len(alt["caption"]) > 5)
        self.assertIn("visual_analysis", d)
        print(f"[PASS] Instagram Caption + 4 Alternatives verified with separate hashtags: {d['hashtags']}")

    def test_06_generate_twitter_concise(self):
        res = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "twitter", "language": "en"}
        )
        self.assertEqual(res.status_code, 200)
        d = res.json()
        self.assertEqual(d["platform"]["id"], "twitter")
        self.assertLessEqual(len(d["caption"]), 280)
        print(f"[PASS] X/Twitter Post verified under 280 chars: ({len(d['caption'])} chars)")

    def test_07_generate_linkedin_professional(self):
        res = self.client.post(
            "/api/generate",
            files={"file": ("tech.jpg", self.tech_img, "image/jpeg")},
            data={"platform": "linkedin", "language": "en"}
        )
        self.assertEqual(res.status_code, 200)
        d = res.json()
        self.assertEqual(d["platform"]["id"], "linkedin")
        self.assertTrue(len(d["caption"]) > 50)
        print("[PASS] LinkedIn Post verified with professional framing")

    def test_08_generate_whatsapp_status(self):
        res = self.client.post(
            "/api/generate",
            files={"file": ("tech.jpg", self.tech_img, "image/jpeg")},
            data={"platform": "whatsapp", "language": "en"}
        )
        self.assertEqual(res.status_code, 200)
        d = res.json()
        self.assertEqual(d["platform"]["id"], "whatsapp")
        self.assertLess(len(d["caption"].splitlines()), 4)
        print(f"[PASS] WhatsApp Status verified: {d['caption']}")

    def test_09_multilingual_telugu_hindi(self):
        # Telugu
        res_te = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "caption", "language": "te"}
        )
        self.assertEqual(res_te.status_code, 200)
        d_te = res_te.json()
        self.assertEqual(d_te["language"]["code"], "te")
        self.assertTrue(len(d_te["caption"]) > 10)

        # Hindi
        res_hi = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "caption", "language": "hi"}
        )
        self.assertEqual(res_hi.status_code, 200)
        d_hi = res_hi.json()
        self.assertEqual(d_hi["language"]["code"], "hi")
        self.assertTrue(len(d_hi["caption"]) > 10)
        print("[PASS] Multilingual generation verified in Telugu and Hindi")

    def test_10_user_instruction_and_variation(self):
        res_v0 = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "instagram", "language": "en", "instruction": "Make it funny", "variation": 0}
        )
        self.assertEqual(res_v0.status_code, 200)

        res_v1 = self.client.post(
            "/api/generate",
            files={"file": ("mountains.jpg", self.mountains_img, "image/jpeg")},
            data={"platform": "instagram", "language": "en", "instruction": "Make it funny", "variation": 1}
        )
        self.assertEqual(res_v1.status_code, 200)
        
        # Regeneration should produce genuinely different content
        cap0 = res_v0.json()["caption"]
        cap1 = res_v1.json()["caption"]
        self.assertNotEqual(cap0, cap1)
        print("[PASS] User instruction & regeneration variation verified (distinct captions)")

    def test_11_tts_audio_streaming(self):
        res = self.client.get("/api/tts?text=Image+Caption+AI+test&lang=en")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "audio/mpeg")
        self.assertGreater(len(res.content), 1000)
        print("[PASS] TTS Audio stream verified")

if __name__ == "__main__":
    unittest.main()
