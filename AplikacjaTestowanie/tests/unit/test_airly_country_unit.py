from unittest.mock import patch
from app.services.air_quality_service import get_aqi


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_airly")
def test_airly_unit_when_poland(mock_airly, mock_country):
    mock_country.return_value = "PL"
    mock_airly.return_value = 8.0

    result = get_aqi("Kraków")

    assert result["pm25"] == 8.0
    assert result["source"] == "Airly"
