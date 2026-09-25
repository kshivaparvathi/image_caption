"""
Image Caption AI - Application Server Entry Point.
FastAPI service serving open-source multimodal BLIP vision endpoints
and responsive modern web application across all platform routes.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

from app.config import settings
from app.routers import config_api, vision, tts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("imagecaption")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include Routers
app.include_router(config_api.router)
app.include_router(vision.router)
app.include_router(tts.router)

# Route all platform pages to index.html for client-side SPA routing
@app.get("/", include_in_schema=False)
@app.get("/instagram", include_in_schema=False)
@app.get("/twitter", include_in_schema=False)
@app.get("/linkedin", include_in_schema=False)
@app.get("/facebook", include_in_schema=False)
@app.get("/whatsapp", include_in_schema=False)
@app.get("/caption", include_in_schema=False)
async def serve_index():
    """Serve the single-page application frontend for all platform routes."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Image Caption AI is operational. Frontend index.html not yet found."}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.app_name} on http://{settings.host}:{settings.port}")
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
