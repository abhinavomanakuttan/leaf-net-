"""
Multi-Agent Disease Intelligence Platform — FastAPI Backend

Endpoints:
  POST /api/vision/analyze     — Image upload → HF disease classification
  GET  /api/climate/risk       — Weather data → outbreak risk scoring
  GET  /api/satellite/health   — Vegetation health index
  POST /api/orchestrate        — Multi-agent synthesis via Groq LLM
  GET  /api/health             — Health check
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from agents.vision_agent import analyze_image
from agents.climate_agent import get_climate_risk
from agents.satellite_agent import get_satellite_health
from agents.orchestrator import run_orchestration
from models.schemas import AgentInput

app = FastAPI(
    title="Disease Intelligence Platform API",
    description="Multi-agent backend for plant disease detection, climate risk, and satellite health.",
    version="1.0.0",
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ──
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": ["vision", "climate", "satellite", "orchestrator"],
    }


# ── Vision Detection Agent ──
@app.post("/api/vision/analyze")
async def vision_analyze(file: UploadFile = File(...)):
    """Upload a plant leaf image for disease classification."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (JPEG, PNG, etc.)")

    try:
        image_bytes = await file.read()
        result = await analyze_image(image_bytes)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision analysis failed: {str(e)}")


# ── Climate Risk Agent ──
@app.get("/api/climate/risk")
async def climate_risk(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
):
    """Fetch real-time weather and compute outbreak risk for given coordinates."""
    try:
        result = await get_climate_risk(lat, lon)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Climate analysis failed: {str(e)}")


# ── Satellite Health Agent ──
@app.get("/api/satellite/health")
async def satellite_health(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
):
    """Fetch vegetation health data for given coordinates."""
    try:
        result = await get_satellite_health(lat, lon)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite analysis failed: {str(e)}")


# ── Orchestration Engine ──
@app.post("/api/orchestrate")
async def orchestrate(agent_input: AgentInput):
    """Synthesize all agent outputs using Groq LLM for unified recommendations."""
    try:
        result = await run_orchestration(agent_input.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")
