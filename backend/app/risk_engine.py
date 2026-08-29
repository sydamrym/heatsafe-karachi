from typing import Dict, List, Any, Optional
from app.models import RiskAssessment

def calculate_risk(apparent_temp: Optional[float], wet_bulb: Optional[float], 
                   heat_index: Optional[float], dry_temp: float) -> RiskAssessment:
    """
    Calculate heat risk based on multiple thermal indices.
    Wet bulb is the most critical for human survivability.
    """
    # Use the most severe indicator
    wb = wet_bulb or 0
    at = apparent_temp or dry_temp
    hi = heat_index or dry_temp

    # Wet-bulb thresholds (most important)
    if wb >= 32:
        return RiskAssessment(
            risk_level="EXTREME",
            risk_color="#7f1d1d",  # dark red
            message="EMERGENCY: Wet-bulb temperature exceeds human survivability. Outdoor activity is life-threatening.",
            actions=[
                "Declare emergency heat alert immediately",
                "All outdoor work must stop",
                "Open emergency cooling centers",
                "Check on elderly and vulnerable populations"
            ],
            apparent_temp=at,
            wet_bulb=wb,
            heat_index=hi
        )
    elif wb >= 28:
        return RiskAssessment(
            risk_level="DANGER",
            risk_color="#dc2626",  # red
            message="DANGER: Wet-bulb temperature is near the human limit. Extended outdoor exposure is hazardous.",
            actions=[
                "Outdoor workers must take mandatory 15-min cooling breaks every hour",
                "Schools should hold students indoors and delay dismissal",
                "Vulnerable individuals should not go outside",
                "Activate community hydration stations"
            ],
            apparent_temp=at,
            wet_bulb=wb,
            heat_index=hi
        )
    elif at >= 40 or hi >= 40:
        return RiskAssessment(
            risk_level="HIGH",
            risk_color="#ea580c",  # orange
            message="HIGH RISK: Extreme heat conditions. Outdoor activity should be severely limited.",
            actions=[
                "Limit outdoor work to early morning hours (before 9 AM)",
                "Children and elderly should remain indoors",
                "Increase fluid intake every 20 minutes",
                "Wear light-colored, loose clothing"
            ],
            apparent_temp=at,
            wet_bulb=wb,
            heat_index=hi
        )
    elif at >= 35 or hi >= 35:
        return RiskAssessment(
            risk_level="CAUTION",
            risk_color="#facc15",  # yellow
            message="CAUTION: High heat. Strenuous outdoor activity should be limited.",
            actions=[
                "Take frequent breaks in shade or air-conditioned spaces",
                "Schedule outdoor activities before 11 AM or after 5 PM",
                "Watch for signs of heat exhaustion"
            ],
            apparent_temp=at,
            wet_bulb=wb,
            heat_index=hi
        )
    else:
        return RiskAssessment(
            risk_level="SAFE",
            risk_color="#22c55e",  # green
            message="SAFE: Normal heat conditions. Standard precautions apply.",
            actions=[
                "Stay hydrated",
                "Normal outdoor activity is safe"
            ],
            apparent_temp=at,
            wet_bulb=wb,
            heat_index=hi
        )

def get_landmark_risk_actions(area_name: str, risk_level: str, landmarks: List[Dict[str, Any]]) -> List[str]:
    """Generate context-specific actions based on landmarks in the area"""
    actions = []

    schools = [l for l in landmarks if l.get("type") == "school"]
    markets = [l for l in landmarks if l.get("type") == "market"]
    construction = [l for l in landmarks if l.get("type") == "construction"]
    hospitals = [l for l in landmarks if l.get("type") == "hospital"]

    if risk_level in ["EXTREME", "DANGER"]:
        if schools:
            actions.append(f"🎓 URGENT: Hold {len(schools)} school(s) indoors. Do not dismiss students until temperatures drop.")
        if construction:
            actions.append(f"🏗️ SUSPEND work at {len(construction)} construction site(s). Heat stroke risk is critical.")
        if markets:
            actions.append(f"🛒 Advise {len(markets)} outdoor market(s) to close during peak hours (11 AM–5 PM).")
        if hospitals:
            actions.append(f"🏥 Alert {len(hospitals)} hospital(s): Expect heat-related emergency admissions.")
    elif risk_level == "HIGH":
        if schools:
            actions.append(f"🎓 Limit outdoor play at {len(schools)} school(s). Ensure classrooms are ventilated.")
        if construction:
            actions.append(f"🏗️ Mandate cooling breaks at {len(construction)} construction site(s) every 45 minutes.")

    return actions

def determine_safest_window(area_stats: Dict[str, Any]) -> str:
    """Recommend safest time window based on current conditions"""
    max_temp = area_stats.get("max", 35)

    if max_temp > 42:
        return "6:00 AM – 8:00 AM ONLY. All other hours are dangerous."
    elif max_temp > 38:
        return "6:00 AM – 9:00 AM and after 7:00 PM."
    elif max_temp > 35:
        return "Before 11:00 AM and after 5:00 PM."
    else:
        return "All day is manageable, but avoid 12:00 PM – 3:00 PM."
