from unittest.mock import patch
from app.services.airly_service import get_aqi_airly


@patch("app.services.airly_service.requests.get")
def test_airly_returns_none_when_no_installations(mock_requests_get):
    """
    Airly:
    - brak instalacji → None
    """

    mock_resp = mock_requests_get.return_value
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = []

    result = get_aqi_airly("NieistniejaceMiasto")

    assert result is None
