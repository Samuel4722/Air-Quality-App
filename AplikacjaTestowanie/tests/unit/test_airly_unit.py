from unittest.mock import patch
from app.services.airly_service import get_aqi_airly


@patch("app.services.airly_service.requests.get")
def test_airly_returns_pm25(mock_get):
    """
    Test jednostkowy:
    - mockujemy oba requesty Airly
    - sprawdzamy, czy funkcja zwraca PM2.5
    """

    # 1. Mock instalacji
    mock_get.return_value.json.side_effect = [
        [{"address": {"city": "Warszawa"}, "id": 123}],
        {"current": {"values": [{"value": 15.0}]}}
    ]
    mock_get.return_value.raise_for_status.return_value = None

    result = get_aqi_airly("Warszawa")
    assert result == 15.0
