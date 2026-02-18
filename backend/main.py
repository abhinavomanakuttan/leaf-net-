"""
Multi-Agent Disease Intelligence Platform — FastAPI Backend

Endpoints:
  POST /api/vision/analyze          — Image upload → HF disease classification
  GET  /api/climate/risk            — Weather data → outbreak risk scoring
  GET  /api/satellite/health        — Vegetation health index
  POST /api/orchestrate             — Multi-agent synthesis via Groq LLM
  GET  /api/market/intelligence     — Mandi price + signals + recommendation
  GET  /api/health                  — Health check
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from agents.vision_agent import analyze_image
from agents.climate_agent import get_climate_risk
from agents.satellite_agent import get_satellite_health
from agents.orchestrator import run_orchestration
from domains.market import (
    get_market_data,
    get_price_trend_series,
    get_available_filters,
    enrich_market_data,
    compute_trade_recommendation,
    to_market_summary,
    to_chart_series,
    resolve_coords_for_state,
)
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



# ── Market Filters ──
@app.get("/api/market/filters")
async def market_filters():
    """Return topology (State->District) and commodities from CSV filenames."""
    try:
        return get_available_filters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filter discovery failed: {str(e)}")


# ── Market Intelligence (Domain Layer) ──
@app.get("/api/market/intelligence")
async def market_intelligence(
    region:    str = Query("Kerala_Kottayam", description="Region filename (e.g. Kerala_Kottayam)"),
    commodity: str = Query("Banana",          description="Commodity name (e.g. Banana)"),
    days:      int = Query(14,                description="Days of price history", ge=1, le=30),
):
    """
    Full market intelligence: price card + trend chart + trade recommendation.
    Powered by uploaded CSV files (backend/data/*.csv).
    """
    import asyncio
    try:
        raw, series = await asyncio.gather(
            get_market_data(region, commodity),
            get_price_trend_series(region, commodity, days=days),
        )
        from domains.market.market_signals import compute_price_momentum
        enriched       = enrich_market_data(raw, series)
        momentum       = compute_price_momentum(series)
        enriched["momentum"] = momentum
        recommendation = compute_trade_recommendation(
            trend        = enriched.get("trend", "stable"),
            buyer_signal = enriched.get("buyer_signal", "Stable"),
            momentum     = momentum.get("momentum", "neutral"),
        )
        chart   = to_chart_series(series)
        summary = to_market_summary(enriched, recommendation)
        summary["chart"] = chart
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market intelligence failed: {str(e)}")


# ── Legacy: raw market data ──
@app.get("/api/market/data")
async def market_data(
    region:    str = Query("Kerala_Kottayam"),
    commodity: str = Query("Banana"),
):
    """Raw market data from CSV."""
    try:
        return await get_market_data(region, commodity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data fetch failed: {str(e)}")



