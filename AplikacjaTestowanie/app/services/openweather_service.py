import os
import requests
from app.core.config import settings


API_KEY = settings.OPENWEATHER_API_KEY


if not API_KEY:
    raise RuntimeError("Brak klucza OPENWEATHER_API_KEY w pliku .env")


def geocode_city(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None
    return data[0]["lat"], data[0]["lon"]


def get_aqi_openweather(city: str):
    coords = geocode_city(city)
    if not coords:
        return None

    lat, lon = coords
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    try:
        return float(data["list"][0]["components"]["pm2_5"])
    except:
        return None
