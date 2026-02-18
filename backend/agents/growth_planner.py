"""
Farmer Growth Planner Agent
Uses Groq (Llama 3.3 70B) to generate a personalised "Profit Roadmap"
including government subsidy schemes, technology recommendations,
and an economic growth strategy for small/medium-scale farmers.
"""

import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPT = """You are an expert Indian agricultural economist and government-scheme advisor.
Given a farmer's profile you MUST respond with ONLY valid JSON (no markdown, no explanation outside JSON) matching this exact structure:

{
  "subsidy_schemes": [
    {
      "title": "<scheme name>",
      "ministry": "<issuing ministry or department>",
      "description": "<1-2 sentence summary>",
      "eligibility": "<who can apply>",
      "benefit": "<₹ amount or percentage>",
      "apply_url": "<official URL or 'Contact local agriculture office'>",
      "eligible": true
    }
  ],
  "technology_advisor": [
    {
      "name": "<technology name, e.g. Drip Irrigation>",
      "category": "<Irrigation|Precision Ag|Protected Cultivation|Post-Harvest|Mechanization|Digital>",
      "investment": "<estimated cost range in ₹>",
      "roi_period": "<estimated payback period>",
      "reasoning": "<why this is recommended for this farmer>",
      "priority": "High|Medium|Low"
    }
  ],
  "economic_strategy": {
    "title": "<short strategy name>",
    "summary": "<2-3 sentence growth roadmap>",
    "year1_actions": ["<action1>", "<action2>", "<action3>"],
    "year2_actions": ["<action1>", "<action2>"],
    "year3_target": "<what the farmer should achieve by year 3>",
    "estimated_income_boost": "<percentage or ₹ range>"
  },
  "risk_warnings": ["<risk 1>", "<risk 2>"]
}

Rules:
- Recommend 3-5 real Indian government schemes (PM-KISAN, PKVY, PMFBY, RKVY, MIDH, etc.) relevant to the farmer's profile.
- Mark "eligible": true/false based on land size, experience, and infrastructure.
- Recommend 3-4 technologies that match the farmer's capital and risk appetite.
- The economic strategy should be realistic, actionable, and specific to the region/crop context.
- Always include at least 1-2 risk warnings.
- All monetary values should be in Indian Rupees (₹).
"""


async def generate_growth_roadmap(profile: dict) -> dict:
    """
    Generate a personalised profit roadmap from a farmer profile.

    Expected profile keys:
      - experience_level: "beginner" | "intermediate" | "experienced"
      - land_size: str, e.g. "2-5 acres"
      - available_capital: str, e.g. "₹50,000 - ₹2,00,000"
      - risk_appetite: "conservative" | "moderate" | "aggressive"
      - irrigation: bool
      - cold_storage: bool
      - region: str (optional, e.g. "Kerala")
      - primary_crop: str (optional, e.g. "Banana")
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")

    user_message = "Generate a Profit Roadmap for the following farmer profile:\n\n"
    user_message += f"Experience Level: {profile.get('experience_level', 'beginner')}\n"
    user_message += f"Land Size: {profile.get('land_size', '1-2 acres')}\n"
    user_message += f"Available Capital: {profile.get('available_capital', 'Under ₹50,000')}\n"
    user_message += f"Risk Appetite: {profile.get('risk_appetite', 'conservative')}\n"
    user_message += f"Has Irrigation: {'Yes' if profile.get('irrigation') else 'No'}\n"
    user_message += f"Has Cold Storage: {'Yes' if profile.get('cold_storage') else 'No'}\n"

    if profile.get("region"):
        user_message += f"Region: {profile['region']}\n"
    if profile.get("primary_crop"):
        user_message += f"Primary Crop: {profile['primary_crop']}\n"

    user_message += "\nProvide a comprehensive, realistic roadmap with Indian government schemes."

    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        model=GROQ_MODEL,
        temperature=0.4,
        max_tokens=3000,
        response_format={"type": "json_object"},
    )

    response_text = chat_completion.choices[0].message.content

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        result = {
            "subsidy_schemes": [],
            "technology_advisor": [],
            "economic_strategy": {
                "title": "Review Required",
                "summary": "Could not parse AI response. Please try again.",
                "year1_actions": [],
                "year2_actions": [],
                "year3_target": "N/A",
                "estimated_income_boost": "N/A",
            },
            "risk_warnings": ["AI response format error — please retry."],
        }

    return result
