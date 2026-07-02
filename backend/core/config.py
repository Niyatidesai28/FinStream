import os
from typing import List


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FinStream")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    WS_URL: str = os.getenv("WS_URL", "ws://localhost:8000/ws/prices")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    @staticmethod
    def cors_origins() -> List[str]:
        raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


settings = Settings()
