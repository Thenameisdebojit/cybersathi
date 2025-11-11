import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    DEBUG: bool = True
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"
    
    DATABASE_URL: str = "sqlite:///./cybersathi.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    META_VERIFY_TOKEN: str = "cybersathi_verify_token_dev"
    META_ACCESS_TOKEN: str = "test_access_token"
    META_APP_SECRET: str = "test_app_secret"
    META_PHONE_NUMBER_ID: str = "test_phone_id"
    META_BUSINESS_ACCOUNT_ID: str = "test_business_id"
    WHATSAPP_API_VERSION: str = "v18.0"
    
    NCRP_API_URL: str = "http://localhost:8001/api"
    NCRP_CLIENT_ID: str = "dev_client_id"
    NCRP_CLIENT_SECRET: str = "dev_client_secret"
    NCRP_API_KEY: str = "dev_api_key"
    
    SECRET_KEY: str = "dev_secret_key_change_in_production_1234567890abcdef"
    ENCRYPTION_KEY: str = "dev_encryption_key_256_bit_change_in_prod_12345678"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    RASA_API_URL: str = "http://localhost:5005"
    RASA_MODEL_PATH: str = "./rasa/models"
    
    HELPLINE_NUMBER: str = "1930"
    HELPLINE_EMAIL: str = "support@cybercrime.gov.in"
    
    ADMIN_EMAIL: str = "admin@cybersathi.in"
    ADMIN_PASSWORD: str = "admin123"
    
    SMS_API_KEY: str = "dev_sms_key"
    EMAIL_SERVICE_API_KEY: str = "dev_email_key"


settings = Settings()
