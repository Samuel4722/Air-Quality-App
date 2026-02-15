import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.e2e
@pytest.mark.skipif(
    not os.getenv("OPENWEATHER_API_KEY"),
    reason="Brak klucza API – test E2E pominięty"
)
def test_e2e_real_openweather():
    """
    TEST E2E (end-to-end)
    -------------------------------------------------
    Scenariusz:
    1. Użytkownik wywołuje endpoint /air-quality/Tokyo
    2. Aplikacja wykrywa kraj (JP)
    3. Aplikacja pomija Airly
    4. Aplikacja pobiera dane z OpenWeather (prawdziwe API)
    5. Zwraca poprawną strukturę JSON

    Ten test NIE używa mocków — to prawdziwy E2E.
    """

    response = client.get("/air-quality/Tokyo")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Tokyo"
    assert data["source"] == "OpenWeather"
    assert isinstance(data["pm25"], (int, float))
