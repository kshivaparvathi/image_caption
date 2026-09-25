"""
VisionCaption AI - Application Launcher
Executes the FastAPI server with Uvicorn.
"""

import sys
import uvicorn
from app.config import settings

def main():
    print("=" * 65)
    print("  VisionCaption AI - Multilingual Image Understanding Platform")
    print("=" * 65)
    print(f"  Version:     {settings.app_version}")
    print(f"  Server URL:  http://{settings.host}:{settings.port}")
    print(f"  API Docs:    http://{settings.host}:{settings.port}/docs")
    print(f"  Languages:   63 Verified Global Languages with Spoken Voice")
    print(f"  TTS Engine:  Google Text-to-Speech (gTTS) & Web Speech API")
    print("=" * 65)
    print("  Press Ctrl+C to terminate the server.\n")

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

if __name__ == "__main__":
    main()
