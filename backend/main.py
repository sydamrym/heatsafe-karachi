from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.routers import heatmap

app = FastAPI(
    title="HeatSafe Karachi API",
    description="AI-powered hyperlocal heat risk platform for Karachi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heatmap.router)

@app.get("/")
async def root():
    return {
        "message": "HeatSafe Karachi API is running",
        "docs": "/docs",
        "endpoints": {
            "areas": "/api/areas",
            "dashboard": "/api/dashboard?date=2026-08-29&time=14:00",
            "area_detail": "/api/area/{area_id}"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
