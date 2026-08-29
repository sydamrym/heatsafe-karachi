import httpx
from typing import Dict, Any, Optional
from app.config import OPENAI_API_KEY

async def generate_ai_summary(area_name: str, temp_stats: Dict[str, Any], 
                               risk: Dict[str, Any], landmarks: list) -> str:
    """Generate natural language summary using OpenAI"""
    if not OPENAI_API_KEY:
        return generate_fallback_summary(area_name, temp_stats, risk, landmarks)

    landmark_str = ", ".join([f"{l['name']} ({l['type']})" for l in landmarks[:5]]) or "residential area"

    prompt = f"""You are a public health AI assistant for Karachi, Pakistan. Write a 2-3 sentence alert about extreme heat.

Area: {area_name}
Temperature range: {temp_stats.get('min', 'N/A')}°C to {temp_stats.get('max', 'N/A')}°C
Average: {temp_stats.get('mean', 'N/A')}°C
Risk level: {risk['risk_level']}
Key landmarks: {landmark_str}

Rules:
- Be urgent but not alarmist
- Mention specific actions for residents
- Keep it under 60 words
- Use simple language that anyone can understand
"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return generate_fallback_summary(area_name, temp_stats, risk, landmarks)

def generate_fallback_summary(area_name: str, temp_stats: Dict[str, Any], 
                               risk: Dict[str, Any], landmarks: list) -> str:
    """Fallback when OpenAI is unavailable"""
    max_t = temp_stats.get('max', 'unknown')
    level = risk['risk_level']

    summaries = {
        "EXTREME": f"{area_name} is experiencing EXTREME heat at {max_t}°C. This is life-threatening. Stay indoors, drink water, and check on neighbors.",
        "DANGER": f"{area_name} is in DANGER zone at {max_t}°C. Outdoor work must stop. Schools should keep students inside. Seek cool shelter immediately.",
        "HIGH": f"{area_name} is very hot at {max_t}°C. Limit outdoor time. Take breaks every 30 minutes. Children and elderly should stay indoors.",
        "CAUTION": f"{area_name} is hot at {max_t}°C. Avoid strenuous activity between 11 AM and 5 PM. Stay hydrated and wear light clothing.",
        "SAFE": f"{area_name} is at safe temperatures around {max_t}°C. Normal activities are fine, but stay hydrated."
    }
    return summaries.get(level, f"{area_name} current temperature: {max_t}°C. {risk['message']}")
