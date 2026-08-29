from fastapi import APIRouter, HTTPException
from typing import Optional
from app.fortyguard_client import get_full_heatmap, get_env_params
from app.risk_engine import calculate_risk, get_landmark_risk_actions, determine_safest_window
from app.ai_recommendations import generate_ai_summary
from app.data import KARACHI_AREAS, MOCK_HEATMAP_DATA
from app.models import DashboardResponse, AreaInsight
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api", tags=["heatmap"])

USE_MOCK = False  # Set to True for offline demo

@router.get("/areas")
async def list_areas():
    """List all available Karachi areas"""
    return {
        "areas": [
            {
                "id": k,
                "name": v["name"],
                "description": v["description"],
                "landmark_count": len(v["landmarks"])
            }
            for k, v in KARACHI_AREAS.items()
        ]
    }

@router.get("/dashboard")
async def get_dashboard(date: Optional[str] = None, time: Optional[str] = "14:00"):
    """
    Get full dashboard data for all Karachi areas.
    This is the MAIN endpoint your frontend calls.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    areas_data = []

    for area_id, area_info in KARACHI_AREAS.items():
        try:
            if USE_MOCK:
                heatmap_result = MOCK_HEATMAP_DATA.get(area_id, {
                    "temperature_stats": {"min": 35, "max": 40, "mean": 37.5}
                })
                env_data = {"data": [{"apparent_temperature": 39, "wet_bulb_temperature": 27, "heat_index": 40}]}
            else:
                # Get heatmap for the area
                heatmap_result = await get_full_heatmap(
                    area_info["polygon"], date, time, granularity=100
                )

                # Get environmental params for center of area (approximate)
                center_lat = area_info["landmarks"][0]["lat"] if area_info["landmarks"] else 24.85
                center_lon = area_info["landmarks"][0]["lon"] if area_info["landmarks"] else 67.0
                env_data = await get_env_params(center_lat, center_lon, date, time)

            temp_stats = heatmap_result.get("temperature_stats", {})
            min_t = temp_stats.get("min", 35)
            max_t = temp_stats.get("max", 40)
            mean_t = temp_stats.get("mean", 37.5)

            # Extract env params
            env_list = env_data.get("data", [{}])
            env = env_list[0] if env_list else {}
            apparent = env.get("apparent_temperature")
            wet_bulb = env.get("wet_bulb_temperature")
            heat_index = env.get("heat_index")

            # Calculate risk
            risk = calculate_risk(apparent, wet_bulb, heat_index, mean_t)

            # Add landmark-specific actions
            landmark_actions = get_landmark_risk_actions(
                area_info["name"], risk.risk_level, area_info["landmarks"]
            )
            risk.actions = landmark_actions + risk.actions

            # AI summary
            ai_summary = await generate_ai_summary(
                area_info["name"], temp_stats, risk.dict(), area_info["landmarks"]
            )

            # Safest window
            safest = determine_safest_window(temp_stats)

            areas_data.append(AreaInsight(
                area_name=area_info["name"],
                temperature_stats=temp_stats,
                risk=risk,
                ai_summary=ai_summary,
                landmarks=area_info["landmarks"],
                safest_window=safest
            ))

        except Exception as e:
            # Graceful fallback for one area failing
            areas_data.append(AreaInsight(
                area_name=area_info["name"],
                temperature_stats={"min": "--", "max": "--", "mean": "--", "error": str(e)},
                risk=calculate_risk(None, None, None, 37),
                ai_summary=f"Data temporarily unavailable for {area_info['name']}. Using cached estimates.",
                landmarks=area_info["landmarks"],
                safest_window="Check local news for heat advisories."
            ))

    # City-wide alert
    max_risk = max([a.risk.risk_level for a in areas_data], key=lambda x: ["SAFE","CAUTION","HIGH","DANGER","EXTREME"].index(x) if x in ["SAFE","CAUTION","HIGH","DANGER","EXTREME"] else 0)
    city_alert = None
    if max_risk in ["DANGER", "EXTREME"]:
        city_alert = f"⚠️ CITY-WIDE HEAT ALERT: Multiple areas in Karachi are experiencing {max_risk} level heat. Avoid outdoor activity."

    return DashboardResponse(
        city="Karachi",
        timestamp=f"{date} {time}",
        areas=areas_data,
        city_wide_alert=city_alert
    )

@router.get("/area/{area_id}")
async def get_area_detail(area_id: str, date: Optional[str] = None, time: Optional[str] = "14:00"):
    """Get detailed data for a single area including GeoJSON tiles"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    if area_id not in KARACHI_AREAS:
        raise HTTPException(status_code=404, detail="Area not found")

    area_info = KARACHI_AREAS[area_id]

    try:
        if USE_MOCK:
            heatmap_result = MOCK_HEATMAP_DATA.get(area_id, {
                "temperature_stats": {"min": 35, "max": 40, "mean": 37.5},
                "geojson": None
            })
        else:
            heatmap_result = await get_full_heatmap(
                area_info["polygon"], date, time, granularity=100
            )

        return {
            "area_id": area_id,
            "name": area_info["name"],
            "temperature_stats": heatmap_result.get("temperature_stats"),
            "geojson": heatmap_result.get("geojson"),  # For map rendering
            "landmarks": area_info["landmarks"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch heatmap: {str(e)}")
