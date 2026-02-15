from unittest.mock import patch
from app.services.openweather_service import get_aqi_openweather
from app.services.air_quality_service import get_aqi


@patch("app.services.openweather_service.requests.get")
def test_openweather_returns_pm25(mock_requests_get):
    """
    Test jednostkowy get_aqi_openweather:
    - mock geocoding
    - mock air pollution
    """

    mock_resp = mock_requests_get.return_value
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.side_effect = [
        [{"lat": 35.0, "lon": 139.0}],  # geocode
        {"list": [{"components": {"pm2_5": 18.6}}]},  # air pollution
    ]

    result = get_aqi_openweather("Tokyo")

    assert result == 18.6


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_openweather")
def test_openweather_unit_when_not_poland(
    mock_get_aqi_openweather, mock_get_country
):
    """
    Test logiki get_aqi:
    - gdy kraj != PL → używamy OpenWeather
    """

    mock_get_country.return_value = "JP"
    mock_get_aqi_openweather.return_value = 22.0

    result = get_aqi("Tokyo")

    assert result["pm25"] == 22.0
    assert result["source"] == "OpenWeather"
