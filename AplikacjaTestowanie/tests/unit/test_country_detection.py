from unittest.mock import patch
from app.services.air_quality_service import get_country_for_city


@patch("app.services.air_quality_service.requests.get")
def test_country_detection_success(mock_requests_get):
    mock_resp = mock_requests_get.return_value
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = [{"country": "JP"}]

    country = get_country_for_city("Tokyo")

    assert country == "JP"


@patch("app.services.air_quality_service.requests.get")
def test_country_detection_no_results(mock_requests_get):
    mock_resp = mock_requests_get.return_value
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = []

    country = get_country_for_city("NieistniejaceMiasto")

    assert country is None
