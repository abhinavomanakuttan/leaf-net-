"""
Vision Detection Agent
Uses Hugging Face Inference API to classify plant diseases from leaf images.
"""

from datetime import datetime
import httpx
from config import HF_API_TOKEN, HF_VISION_MODEL


# ── Severity heuristic based on confidence ──
def _estimate_severity(confidence: float) -> str:
    if confidence >= 90:
        return "Stage 4 — Severe / Advanced"
    elif confidence >= 75:
        return "Stage 3 — Moderate Spread"
    elif confidence >= 50:
        return "Stage 2 — Early Development"
    else:
        return "Stage 1 — Initial Onset"


# ── Clean up HF model labels ──
def _clean_label(label: str) -> str:
    """Convert labels like 'Tomato___Late_blight' to 'Tomato — Late Blight'."""
    parts = label.replace("___", " — ").replace("_", " ")
    return parts.title()


def _detect_content_type(image_bytes: bytes) -> str:
    """Detect image content type from magic bytes."""
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if image_bytes[:2] == b'\xff\xd8':
        return "image/jpeg"
    if image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        return "image/webp"
    return "image/jpeg"  # default fallback


async def analyze_image(image_bytes: bytes) -> dict:
    """
    Send an image to the Hugging Face plant disease model and return
    structured classification results.
    """
    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN is not set. Please add it to your .env file.")

    api_url = f"https://api-inference.huggingface.co/models/{HF_VISION_MODEL}"
    content_type = _detect_content_type(image_bytes)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            api_url,
            content=image_bytes,
            headers={
                "Authorization": f"Bearer {HF_API_TOKEN}",
                "Content-Type": content_type,
            },
        )
        response.raise_for_status()
        results = response.json()

    if not results or not isinstance(results, list):
        return {
            "disease_name": "No result",
            "confidence": 0.0,
            "severity_stage": "Unknown",
            "top_predictions": [],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        }

    # Build top predictions list
    top_predictions = []
    for r in results[:5]:
        top_predictions.append({
            "label": _clean_label(r["label"]),
            "confidence": round(r["score"] * 100, 2),
        })

    top = results[0]
    confidence = round(top["score"] * 100, 2)

    return {
        "disease_name": _clean_label(top["label"]),
        "confidence": confidence,
        "severity_stage": _estimate_severity(confidence),
        "top_predictions": top_predictions,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    }

