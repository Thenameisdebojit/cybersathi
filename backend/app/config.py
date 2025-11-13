import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False
    )
    
    # Application
    APP_NAME: str = "CyberSathi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    FRONTEND_URL: str = "http://localhost:5173"
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # PostgreSQL Database (from Replit environment)
    # DATABASE_URL is set by Replit automatically
    
    # Redis Cache & Queue
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50
    CACHE_TTL: int = 3600  # 1 hour
    
    # Celery Background Tasks
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # WhatsApp Meta Cloud API
    META_VERIFY_TOKEN: str = "cybersathi_verify_token_dev"
    META_ACCESS_TOKEN: str = "test_access_token"
    META_APP_SECRET: str = "test_app_secret"
    META_PHONE_NUMBER_ID: str = "test_phone_id"
    META_BUSINESS_ACCOUNT_ID: str = "test_business_id"
    WHATSAPP_API_VERSION: str = "v18.0"
    WHATSAPP_API_BASE_URL: str = "https://graph.facebook.com"
    
    # NCRP Integration (National Cybercrime Reporting Portal)
    NCRP_API_URL: str = "https://cybercrime.gov.in/api"
    NCRP_CLIENT_ID: str = "dev_client_id"
    NCRP_CLIENT_SECRET: str = "dev_client_secret"
    NCRP_API_KEY: str = "dev_api_key"
    NCRP_MOCK_MODE: bool = True  # Set False for production
    
    # Security & JWT
    SECRET_KEY: str = "dev_secret_key_change_in_production_1234567890abcdef"
    ENCRYPTION_KEY: str = "dev_encryption_key_256_bit_change_in_prod_12345678"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = "your_google_client_id"
    GOOGLE_CLIENT_SECRET: str = "your_google_client_secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:5000/auth/google/callback"
    
    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Rasa NLP
    RASA_API_URL: str = "http://localhost:5005"
    RASA_MODEL_PATH: str = "./rasa/models"
    RASA_ENABLED: bool = True
    NLP_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Helpline
    HELPLINE_NUMBER: str = "1930"
    HELPLINE_EMAIL: str = "support@cybercrime.gov.in"
    
    # Admin Credentials (First User)
    ADMIN_EMAIL: str = "admin@cybersathi.in"
    ADMIN_PASSWORD: str = "Admin@1930"
    ADMIN_PHONE: str = "+919999999999"
    
    # External Services
    SMS_API_KEY: str = "dev_sms_key"
    SMS_API_URL: str = "https://api.sms-provider.com/send"
    EMAIL_SERVICE_API_KEY: str = "dev_email_key"
    EMAIL_FROM: str = "noreply@cybersathi.in"
    
    # Monitoring & Logging
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    ENABLE_METRICS: bool = True
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "pdf", "doc", "docx"]
    UPLOAD_DIR: str = "./uploads"
    
    # Data Retention
    DATA_RETENTION_DAYS: int = 365
    AUDIT_LOG_RETENTION_DAYS: int = 730
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5000", "http://localhost:3000"]
    
    @property
    def mongodb_connection_string(self) -> str:
        """Get full MongoDB connection string."""
        return f"{self.MONGODB_URL}/{self.MONGODB_DB_NAME}"
    
    @property
    def whatsapp_api_url(self) -> str:
        """Get WhatsApp API endpoint."""
        return f"{self.WHATSAPP_API_BASE_URL}/{self.WHATSAPP_API_VERSION}/{self.META_PHONE_NUMBER_ID}/messages"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
