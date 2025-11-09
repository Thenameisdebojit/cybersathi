# backend/app/config.py
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    DEBUG: bool = True
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # Database: default sqlite for quick local dev
    DATABASE_URL: str = "sqlite:///./cybersathi.db"

    # WhatsApp config (Meta Cloud / Twilio)
    WHATSAPP_API_URL: str = Field(default="", description="WhatsApp provider API base URL")
    WHATSAPP_API_TOKEN: str = Field(default="", description="WhatsApp API bearer token")

    # CyberPortal
    CYBERPORTAL_API_URL: str = Field(default="https://cybercrime.gov.in/api", description="Cybercrime portal API base")
    CYBERPORTAL_API_KEY: str = Field(default="", description="API key for cyber portal (if available)")

    # JWT secret
    JWT_SECRET: str = Field(default="change-me-in-prod", description="JWT secret for tokens")

    # Rasa
    RASA_URL: str = Field(default="http://localhost:5005", description="Rasa server URL")

    ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"