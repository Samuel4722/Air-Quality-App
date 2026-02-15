from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.services.air_quality_service.get_country_for_city")
@patch("app.services.air_quality_service.get_aqi_airly")
def test_airly_used_when_country_is_poland(mock_get_aqi_airly, mock_get_country):
    """
    Integracja:
    - wykrywanie kraju (PL)
    - użycie Airly
    """

    mock_get_country.return_value = "PL"
    mock_get_aqi_airly.return_value = 12.5

    response = client.get("/air-quality/Warszawa")

    assert response.status_code == 200
    assert response.json() == {
        "city": "Warszawa",
        "pm25": 12.5,
        "source": "Airly"
    }
