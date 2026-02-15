from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.cache import CACHE

client = TestClient(app)


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_openweather")
def test_integration_openweather(mock_get_aqi_openweather, mock_get_country):
    """
    Integracja:
    - wykrywanie kraju (JP)
    - użycie OpenWeather
    """

    # Czyszczenie cache, żeby nie brać starej wartości dla Tokyo
    CACHE.clear()

    mock_get_country.return_value = "JP"
    mock_get_aqi_openweather.return_value = 20.0

    response = client.get("/air-quality/Tokyo")

    assert response.status_code == 200
    assert response.json() == {
        "city": "Tokyo",
        "pm25": 20.0,
        "source": "OpenWeather"
    }
