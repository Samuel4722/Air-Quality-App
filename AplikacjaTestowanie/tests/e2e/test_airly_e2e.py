import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.e2e
@pytest.mark.skipif(
    not os.getenv("AIRLY_API_KEY"),
    reason="Brak klucza API – test E2E Airly pominięty"
)
def test_e2e_real_airly():
    """
    TEST E2E (end-to-end) – Airly
    -------------------------------------------------
    Scenariusz:
    1. Użytkownik wywołuje endpoint /air-quality/Krakow
    2. Aplikacja wykrywa kraj (PL)
    3. Aplikacja pomija OpenWeather
    4. Aplikacja pobiera dane z Airly (prawdziwe API)
    5. Zwraca poprawną strukturę JSON

    Ten test NIE używa mocków — to prawdziwy E2E.
    """

    response = client.get("/air-quality/Krakow")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Krakow"
    assert data["source"] == "Airly"
    assert isinstance(data["pm25"], (int, float))
