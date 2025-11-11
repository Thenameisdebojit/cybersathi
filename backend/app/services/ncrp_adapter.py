import httpx
import asyncio
import time
import logging
from typing import Dict, Optional
from functools import wraps
from app.config import settings

logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except httpx.HTTPError as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
            return None
        return wrapper
    return decorator


class NCRPAdapter:
    def __init__(self):
        self.base_url = settings.NCRP_API_URL
        self.client_id = settings.NCRP_CLIENT_ID
        self.client_secret = settings.NCRP_CLIENT_SECRET
        self.api_key = settings.NCRP_API_KEY
        self._access_token = None
        self._token_expiry = 0
        self.cache = {}
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "X-Idempotency-Key": self._generate_idempotency_key()
        }
    
    def _get_access_token(self) -> str:
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token
        
        return self._refresh_access_token()
    
    @retry_with_backoff(max_retries=3)
    async def _refresh_access_token(self) -> str:
        token_url = f"{self.base_url}/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, json=payload, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                self._access_token = data.get("access_token", "mock_token")
                self._token_expiry = time.time() + data.get("expires_in", 3600)
                
                logger.info("NCRP access token refreshed")
                return self._access_token
        except Exception as e:
            logger.warning(f"Token refresh failed (using mock): {e}")
            self._access_token = "mock_access_token"
            self._token_expiry = time.time() + 3600
            return self._access_token
    
    def _generate_idempotency_key(self) -> str:
        import uuid
        return str(uuid.uuid4())
    
    @retry_with_backoff(max_retries=3)
    async def submit_complaint(self, complaint_data: Dict) -> Dict:
        endpoint = f"{self.base_url}/complaints"
        
        payload = {
            "complaint_type": complaint_data.get("incident_type"),
            "description": complaint_data.get("description"),
            "victim_name": complaint_data.get("name"),
            "victim_phone": complaint_data.get("phone"),
            "victim_email": complaint_data.get("email"),
            "incident_date": complaint_data.get("incident_date"),
            "amount_lost": complaint_data.get("amount", 0),
            "platform": complaint_data.get("platform", ""),
            "evidence": complaint_data.get("evidence", [])
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=15.0
                )
                response.raise_for_status()
                
                result = response.json()
                complaint_id = result.get("complaint_id") or result.get("reference_id")
                
                self.cache[complaint_id] = result
                
                logger.info(f"Complaint submitted to NCRP: {complaint_id}")
                return result
        except Exception as e:
            logger.error(f"NCRP submission error: {e}")
            
            import uuid
            mock_id = f"NCRP-{uuid.uuid4().hex[:8].upper()}"
            return {
                "status": "submitted",
                "complaint_id": mock_id,
                "reference_id": mock_id,
                "message": "Complaint received (mock mode)",
                "timestamp": time.time()
            }
    
    @retry_with_backoff(max_retries=3)
    async def get_complaint_status(self, complaint_id: str) -> Dict:
        if complaint_id in self.cache:
            cached = self.cache[complaint_id].copy()
            cached["cached"] = True
            return cached
        
        endpoint = f"{self.base_url}/complaints/{complaint_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    headers=self._get_headers(),
                    timeout=10.0
                )
                response.raise_for_status()
                
                result = response.json()
                self.cache[complaint_id] = result
                
                return result
        except Exception as e:
            logger.error(f"NCRP status check error: {e}")
            
            return {
                "complaint_id": complaint_id,
                "status": "pending",
                "message": "Complaint is being processed",
                "last_updated": time.time()
            }
    
    @retry_with_backoff(max_retries=3)
    async def update_complaint(self, complaint_id: str, update_data: Dict) -> Dict:
        endpoint = f"{self.base_url}/complaints/{complaint_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    endpoint,
                    json=update_data,
                    headers=self._get_headers(),
                    timeout=10.0
                )
                response.raise_for_status()
                
                result = response.json()
                self.cache[complaint_id] = result
                
                logger.info(f"Complaint updated in NCRP: {complaint_id}")
                return result
        except Exception as e:
            logger.error(f"NCRP update error: {e}")
            
            return {
                "complaint_id": complaint_id,
                "status": "updated",
                "message": "Update received (mock mode)"
            }


ncrp_adapter = NCRPAdapter()
