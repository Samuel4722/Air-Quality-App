from app.services.airly_service import get_aqi_airly
from app.services.openweather_service import get_aqi_openweather, geocode_city
from app.services.cache import get_from_cache, set_cache
import requests
import os


def get_country_for_city(city: str):
    """
    Zwraca kod kraju (np. 'PL', 'GB', 'JP') dla podanego miasta.
    """
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"

    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        return None

    return data[0].get("country")


def get_aqi(city: str):
    cache_key = f"aqi:{city.lower()}"
    cached = get_from_cache(cache_key)
    if cached:
        return cached

    #1. Wykrywanie kraju 
    country = get_country_for_city(city)

    #2. Jeśli Polska -> Airly 
    if country == "PL":
        pm25 = get_aqi_airly(city)
        if pm25 is not None:
            result = {"city": city, "pm25": pm25, "source": "Airly"}
            set_cache(cache_key, result)
            return result

    # 3. Reszta świata -> OpenWeather
    pm25 = get_aqi_openweather(city)
    if pm25 is not None:
        result = {"city": city, "pm25": pm25, "source": "OpenWeather"}
        set_cache(cache_key, result)
        return result

    raise ValueError(f"Brak danych PM2.5 dla miasta '{city}'")
