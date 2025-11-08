# backend/app/config.py
from pydantic import BaseSettings, AnyHttpUrl, Field

class Settings(BaseSettings):
    DEBUG: bool = True
    PORT: int = 8000
    FRONTEND_URL: AnyHttpUrl = "http://localhost:5173"

    # Database: default sqlite for quick local dev
    DATABASE_URL: str = "sqlite:///./cybersathi.db"

    # WhatsApp config (Meta Cloud / Twilio)
    WHATSAPP_API_URL: str = Field("", description="WhatsApp provider API base URL")
    WHATSAPP_API_TOKEN: str = Field("", description="WhatsApp API bearer token")

    # CyberPortal
    CYBERPORTAL_API_URL: str = Field("https://cybercrime.gov.in/api", description="Cybercrime portal API base")
    CYBERPORTAL_API_KEY: str = Field("", description="API key for cyber portal (if available)")

    # JWT secret
    JWT_SECRET: str = Field("change-me-in-prod", description="JWT secret for tokens")

    # Rasa
    RASA_URL: str = Field("http://localhost:5005", description="Rasa server URL")

    ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
