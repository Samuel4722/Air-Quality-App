Air Quality App

Aplikacja FastAPI do pobierania jakości powietrza (PM2.5) z dwóch źródeł: Airly (dla Polski) oraz OpenWeather (dla reszty świata).
Projekt zawiera testy jednostkowe, integracyjne i E2E oraz prosty system cache.
1. Funkcjonalność

Aplikacja udostępnia endpoint:
Kod

GET /air-quality/{city}

Działanie:

    Wykrywa kraj miasta (OpenWeather Geocoding API).

    Jeśli kraj to „PL”, pobiera PM2.5 z Airly API.

    Jeśli kraj jest inny, pobiera PM2.5 z OpenWeather Air Pollution API.

    Wynik jest zapisywany w cache (TTL = 5 minut).

    Zwracany jest JSON:

Kod

{
  "city": "Tokyo",
  "pm25": 20.5,
  "source": "OpenWeather"
}

2. Struktura projektu
Kod

app/
 ├── core/
 │    └── config.py
 ├── routers/
 │    └── air_quality.py
 ├── services/
 │    ├── air_quality_service.py
 │    ├── airly_service.py
 │    ├── openweather_service.py
 │    └── cache.py
 └── main.py
tests/
 ├── unit/
 ├── integration/
 └── e2e/
docs/
 ├── raport_pokrycia.txt
 └── raport_testy.txt
pytest.ini
requirements.txt
Dockerfile
docker-compose.yml
start.py

3. Wymagania

    Python 3.12+

    FastAPI

    requests

    python-dotenv

    pytest + pytest-cov

    Docker (opcjonalnie, jeśli chcesz uruchamiać kontenerowo)

Wszystkie zależności znajdują się w pliku:
Kod

requirements.txt

4. Konfiguracja środowiska

Utwórz plik .env w katalogu głównym projektu:
Kod

OPENWEATHER_API_KEY=twoj_klucz
AIRLY_API_KEY=twoj_klucz

Do repozytorium wrzucasz tylko:
Kod

.env.example

5. Uruchamianie aplikacji (lokalnie)
5.1 Instalacja zależności
Kod

pip install -r requirements.txt

5.2 Uruchomienie serwera
Kod

uvicorn app.main:app --reload

Aplikacja będzie dostępna pod adresem:
Kod

http://127.0.0.1:8000

5.3 Dokumentacja API
Kod

http://127.0.0.1:8000/docs

6. Uruchamianie aplikacji w Dockerze

Aplikacja obsługuje zmienne środowiskowe z pliku .env.
6.1 Uruchomienie jednym poleceniem
Kod

docker compose up --build

6.2 Dostęp do aplikacji

    Aplikacja: http://localhost:8000

    Dokumentacja Swagger: http://localhost:8000/docs

7. Testy
7.1 Uruchamianie wszystkich testów
Kod

pytest

7.2 Testy z pokryciem
Kod

pytest --cov=app

Raporty znajdują się w katalogu:
Kod

docs/

8. Logika wyboru źródła danych
Kod

                +----------------------+
                |  /air-quality/{city} |
                +----------+-----------+
                           |
                           v
            +--------------+--------------+
            | Wykryj kraj miasta (OWM)    |
            +--------------+--------------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
   Jeśli kraj == "PL"                Jeśli kraj != "PL"
   użyj Airly API                    użyj OpenWeather API

9. Cache

    Implementacja w pamięci (dict).

    Klucz: aqi:{city}.

    TTL: 300 sekund.

    Wykorzystywany w air_quality_service.py.

10. Cel projektu

Projekt został wykonany jako aplikacja zaliczeniowa na studia.

11. Licencja

Projekt edukacyjny — możesz go rozwijać, modyfikować i wykorzystywać w portfolio.