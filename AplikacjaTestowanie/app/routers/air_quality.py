from fastapi import APIRouter, HTTPException
from app.services.air_quality_service import get_aqi

router = APIRouter(prefix="/air-quality", tags=["air-quality"])


@router.get("/{city}")
def read_air_quality(city: str):
    try:
        return get_aqi(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
