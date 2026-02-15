import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        self.AIRLY_API_KEY = os.getenv("AIRLY_API_KEY")

        if not self.OPENWEATHER_API_KEY:
            raise ValueError("BRAK klucz OPENWEATHER_API_KEY w pliku .env")
        
        if not self.AIRLY_API_KEY:
            raise ValueError("BRAK klucz AIRLY_API_KEY w pliku .env")
        
settings = Settings()

