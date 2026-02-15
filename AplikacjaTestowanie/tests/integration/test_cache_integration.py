from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.cache import CACHE

client = TestClient(app)


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_openweather")
def test_cache_integration(mock_get_aqi_openweather, mock_get_country):
    """
    Integracja z cache:
    - pierwsze wywołanie trafia do OpenWeather
    - drugie wywołanie idzie z cache (brak dodatkowego calla)
    """

    CACHE.clear()

    mock_get_country.return_value = "JP"
    mock_get_aqi_openweather.return_value = 30.0

    first = client.get("/air-quality/Tokyo")
    second = client.get("/air-quality/Tokyo")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert mock_get_aqi_openweather.call_count == 1
