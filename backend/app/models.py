from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class HeatmapRequest(BaseModel):
    area_name: str
    polygon: Dict[str, Any]
    date: str
    time: str = "14:00"
    granularity: int = 100

class EnvParamsRequest(BaseModel):
    lat: float
    lon: float
    date: str
    time: str = "14:00"

class RiskAssessment(BaseModel):
    risk_level: str
    risk_color: str
    message: str
    actions: List[str]
    apparent_temp: Optional[float] = None
    wet_bulb: Optional[float] = None
    heat_index: Optional[float] = None

class AreaInsight(BaseModel):
    area_name: str
    temperature_stats: Dict[str, Any]
    risk: RiskAssessment
    ai_summary: str
    landmarks: List[Dict[str, Any]]
    safest_window: Optional[str] = None

class DashboardResponse(BaseModel):
    city: str
    timestamp: str
    areas: List[AreaInsight]
    city_wide_alert: Optional[str] = None
