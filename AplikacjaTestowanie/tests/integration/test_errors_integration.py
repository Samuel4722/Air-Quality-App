from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.cache import CACHE

client = TestClient(app)


@patch("app.services.air_quality_service.get_aqi")
def test_not_found_error_from_service(mock_get_aqi):
    """
    Integracja:
    - gdy serwis rzuci ValueError, API zwraca 404
    """

    CACHE.clear()

    mock_get_aqi.side_effect = ValueError("Brak danych PM2.5 dla miasta 'MiastoXYZ'")

    response = client.get("/air-quality/MiastoXYZ")

    assert response.status_code == 404
    assert "Brak danych PM2.5" in response.json()["detail"]


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_airly")
@patch("app.services.air_quality_service.get_aqi_openweather")
def test_not_found_when_both_sources_none(
    mock_get_aqi_openweather, mock_get_aqi_airly, mock_get_country
):
    """
    Integracja:
    - Airly zwraca None
    - OpenWeather zwraca None
    - API → 404
    """

    # Czyszczenie cache, żeby nie użył poprzedniego wyniku dla Tokyo
    CACHE.clear()

    mock_get_country.return_value = "JP"
    mock_get_aqi_airly.return_value = None
    mock_get_aqi_openweather.return_value = None

    response = client.get("/air-quality/Tokyo")

    assert response.status_code == 404
    assert "Brak danych PM2.5" in response.json()["detail"]
