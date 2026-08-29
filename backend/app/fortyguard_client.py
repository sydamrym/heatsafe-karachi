import httpx
import asyncio
import time
from typing import Dict, Any, Optional
from app.config import FORTYGUARD_API_KEY, FORTYGUARD_BASE_URL

HEADERS = {
    "api-key": FORTYGUARD_API_KEY,
    "Content-Type": "application/json"
}

async def submit_heatmap(polygon: Dict[str, Any], date: str, time_str: str, granularity: int = 100) -> str:
    """Submit heatmap job and return activity_id"""
    payload = {
        "polygon_aoi": polygon,
        "date_time": {
            "start_date": date,
            "start_time": time_str,
            "filter_type": 1
        },
        "granularity": granularity
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{FORTYGUARD_BASE_URL}/v1/heatmap", headers=HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["data"]["activity_id"]

async def get_status(activity_id: str) -> Dict[str, Any]:
    """Poll status of a heatmap job"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{FORTYGUARD_BASE_URL}/v1/status/{activity_id}", headers=HEADERS)
        resp.raise_for_status()
        return resp.json()

async def poll_heatmap_result(activity_id: str, max_wait: int = 120) -> Optional[Dict[str, Any]]:
    """Poll until completion or timeout"""
    for _ in range(max_wait // 5):
        status = await get_status(activity_id)
        job_status = status["data"]["status"]
        if job_status == "Completed":
            return status["data"]["result"]
        if job_status in ["Failed", "Error"]:
            raise Exception(f"Heatmap job failed: {status}")
        await asyncio.sleep(5)
    raise TimeoutError("Heatmap polling timed out")

async def get_env_params(lat: float, lon: float, date: str, time_str: str) -> Dict[str, Any]:
    """Get environmental parameters for a coordinate"""
    payload = {
        "coordinates": [{"lat": lat, "lon": lon}],
        "date_time": {
            "start_date": date,
            "start_time": time_str,
            "filter_type": 1
        }
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{FORTYGUARD_BASE_URL}/v1/env_params", headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()

async def get_full_heatmap(polygon: Dict[str, Any], date: str, time_str: str, granularity: int = 100) -> Dict[str, Any]:
    """Submit and poll for complete heatmap result"""
    activity_id = await submit_heatmap(polygon, date, time_str, granularity)
    result = await poll_heatmap_result(activity_id)
    return result
