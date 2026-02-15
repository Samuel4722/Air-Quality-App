# Air Quality App

Aplikacja FastAPI do pobierania danych o jakości powietrza (PM2.5) z dwóch źródeł: **Airly** (dla Polski) oraz **OpenWeather** (dla reszty świata).  
Projekt zawiera testy jednostkowe, integracyjne i E2E oraz prosty system cache w pamięci.

---

## Funkcjonalność

### Endpoint

GET /air-quality/{city}

### Jak to działa:

1. Aplikacja wykrywa kraj miasta za pomocą **OpenWeather Geocoding API**.  
2. Jeśli kraj to **PL**, dane PM2.5 pobierane są z **Airly API**.  
3. W przeciwnym przypadku dane pobierane są z **OpenWeather Air Pollution API**.  
4. Wynik jest zapisywany w cache na **5 minut (TTL = 300s)**.  
5. Zwracany jest JSON:

{
  "city": "Tokyo",
  "pm25": 20.5,
  "source": "OpenWeather"
}

---

##  Struktura projektu

app/  
├── core/  
│   └── config.py  
├── routers/  
│   └── air_quality.py  
├── services/  
│   ├── air_quality_service.py  
│   ├── airly_service.py  
│   ├── openweather_service.py  
│   └── cache.py  
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

---

##  Wymagania

- Python 3.12+  
- FastAPI  
- requests  
- python-dotenv  
- pytest + pytest-cov  
- Docker (opcjonalnie)

Wszystkie zależności znajdują się w:  
requirements.txt

---

##  Konfiguracja środowiska

Utwórz plik `.env` w katalogu głównym projektu:

OPENWEATHER_API_KEY=twoj_klucz  
AIRLY_API_KEY=twoj_klucz  

Do repozytorium dodawany jest tylko:  
.env.example

---

##  Uruchamianie aplikacji lokalnie

1. Instalacja zależności:

pip install -r requirements.txt

2. Uruchomienie serwera:

uvicorn app.main:app --reload

Aplikacja dostępna pod adresem:  
http://127.0.0.1:8000

Dokumentacja API:  
http://127.0.0.1:8000/docs

---

##  Uruchamianie aplikacji w Dockerze

Aplikacja korzysta ze zmiennych środowiskowych z pliku `.env`.

Uruchomienie jednym poleceniem:

docker compose up --build

Dostęp:

Aplikacja: http://localhost:8000  
Swagger: http://localhost:8000/docs

---

##  Testy

Uruchomienie wszystkich testów:

pytest

Testy z pokryciem:

pytest --cov=app

Raporty znajdują się w:  
docs/

---

##  Logika wyboru źródła danych

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
Jeśli kraj == "PL"           Jeśli kraj != "PL"  
użyj Airly API               użyj OpenWeather API  

---

## Cache

- Implementacja w pamięci (dict)  
- Klucz: aqi:{city}  
- TTL: 300 sekund  
- Wykorzystywany w air_quality_service.py

---

##  Cel projektu

Projekt został wykonany jako aplikacja zaliczeniowa na studia i może być wykorzystywany jako projekt portfolio.

---

##  Licencja

Projekt edukacyjny — możesz go rozwijać, modyfikować i wykorzystywać w portfolio.
