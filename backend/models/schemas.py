from pydantic import BaseModel
from typing import Optional


# ── Vision Agent ──
class VisionResult(BaseModel):
    disease_name: str
    confidence: float
    severity_stage: str
    top_predictions: list[dict]
    analyzed_at: str


# ── Climate Agent ──
class ClimateResult(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float
    soil_moisture: Optional[float] = None
    risk_level: str
    outbreak_probability: float
    forecast_summary: str
    last_updated: str


# ── Satellite Agent ──
class SatelliteResult(BaseModel):
    ndvi_score: float
    vegetation_stress: str
    health_trend: str
    data_source: str
    coverage_period: str
    last_updated: str


# ── Orchestration ──
class AgentInput(BaseModel):
    vision: Optional[dict] = None
    climate: Optional[dict] = None
    satellite: Optional[dict] = None


class OrchestrationResult(BaseModel):
    agents: list[dict]
    overall_status: str
    consensus_score: float
    risk_level: str
    action_summary: str
    biological_controls: list[dict]
    chemical_advisory: dict
    conflicts: list[str]
    raw_llm_reasoning: Optional[str] = None
