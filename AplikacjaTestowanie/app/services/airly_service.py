import os
import requests
from difflib import get_close_matches
from app.core.config import settings

AIRLY_API_KEY = settings.AIRLY_API_KEY


if not AIRLY_API_KEY:
    raise RuntimeError("Brak klucza AIRLY_API_KEY w pliku .env")

BASE_URL = "https://airapi.airly.eu/v2"


def geocode_city(city: str):
    """
    Wyszukuje instalacje Airly w Polsce i dopasowuje miasto fuzzy search.
    """
    url = f"{BASE_URL}/installations/nearest"
    params = {
        "lat": 52.0,
        "lng": 19.0,
        "maxDistanceKM": 500,
        "maxResults": 1000
    }
    headers = {"apikey": AIRLY_API_KEY}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    
    matches = get_close_matches(city, [i["address"]["city"] for i in data], n=1, cutoff=0.3)
    if not matches:
        return None

    best_city = matches[0]

    
    return [i for i in data if i["address"]["city"] == best_city]


def get_pm25_from_installation(installation_id: int):
    """
    Pobiera PM2.5 z konkretnej instalacji Airly.
    """
    url = f"{BASE_URL}/measurements/installation"
    params = {"installationId": installation_id}
    headers = {"apikey": AIRLY_API_KEY}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    try:
        return data["current"]["values"][0]["value"]  # PM2.5
    except Exception:
        return None


def get_aqi_airly(city: str):
    """
    Pobiera PM2.5 dla miasta z Airly.
    """
    installations = geocode_city(city)

    if not installations:
        return None

    for inst in installations:
        pm25 = get_pm25_from_installation(inst["id"])
        if pm25 is not None:
            return pm25

    return None
