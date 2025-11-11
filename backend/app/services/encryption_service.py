import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from app.config import settings


class EncryptionService:
    def __init__(self):
        self.cipher_suite = self._get_cipher_suite()
    
    def _get_cipher_suite(self):
        key = base64.urlsafe_b64encode(settings.ENCRYPTION_KEY.encode().ljust(32)[:32])
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        if not data:
            return ""
        encrypted = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return ""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher_suite.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def hash_data(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    def encrypt_sensitive_fields(self, data: dict, fields: list) -> dict:
        encrypted_data = data.copy()
        for field in fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encrypt(str(encrypted_data[field]))
        return encrypted_data
    
    def decrypt_sensitive_fields(self, data: dict, fields: list) -> dict:
        decrypted_data = data.copy()
        for field in fields:
            if field in decrypted_data and decrypted_data[field]:
                try:
                    decrypted_data[field] = self.decrypt(str(decrypted_data[field]))
                except:
                    pass
        return decrypted_data


encryption_service = EncryptionService()
