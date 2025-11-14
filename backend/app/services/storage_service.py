# backend/app/services/storage_service.py
"""Storage service for handling file uploads with S3-compatible abstraction."""
import os
import hashlib
from datetime import datetime
from typing import Optional, BinaryIO
from pathlib import Path

from fastapi import UploadFile
from app.config import settings


class StorageService:
    """
    File storage service with S3-compatible abstraction.
    Uses local filesystem by default, can switch to S3 via environment variables.
    """
    
    def __init__(self):
        self.storage_type = "local" if not settings.S3_ENDPOINT else "s3"
        self.local_storage_path = Path(settings.LOCAL_STORAGE_PATH or "data/uploads")
        self.local_storage_path.mkdir(parents=True, exist_ok=True)
        
        if self.storage_type == "s3":
            try:
                import boto3
                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=settings.S3_ENDPOINT,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION or 'us-east-1'
                )
                self.bucket_name = settings.S3_BUCKET_NAME or 'cybersathi-uploads'
            except ImportError:
                print("Warning: boto3 not installed, falling back to local storage")
                self.storage_type = "local"
    
    def _generate_safe_filename(self, original_filename: str) -> str:
        """Generate a safe, unique filename."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        file_hash = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]
        name, ext = os.path.splitext(original_filename)
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_'))[:50]
        return f"{timestamp}_{file_hash}_{safe_name}{ext}"
    
    async def save_file(
        self,
        file: UploadFile,
        folder: str = "complaints"
    ) -> dict:
        """
        Save uploaded file and return metadata.
        
        Args:
            file: FastAPI UploadFile object
            folder: Subfolder to organize files (e.g., 'complaints', 'evidence')
        
        Returns:
            dict with file metadata (url, filename, size, type)
        """
        filename = file.filename or "unnamed_file"
        content_type = file.content_type or "application/octet-stream"
        safe_filename = self._generate_safe_filename(filename)
        file_content = await file.read()
        file_size = len(file_content)
        
        if self.storage_type == "local":
            return await self._save_local(safe_filename, file_content, folder, content_type, file_size)
        else:
            return await self._save_s3(safe_filename, file_content, folder, content_type, file_size)
    
    async def _save_local(
        self,
        filename: str,
        content: bytes,
        folder: str,
        content_type: str,
        file_size: int
    ) -> dict:
        """Save file to local filesystem."""
        folder_path = self.local_storage_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        file_path = folder_path / filename
        file_path.write_bytes(content)
        
        # Return relative URL that can be served by the backend
        relative_url = f"/uploads/{folder}/{filename}"
        
        return {
            "url": relative_url,
            "filename": filename,
            "file_size": file_size,
            "file_type": content_type,
            "storage_type": "local"
        }
    
    async def _save_s3(
        self,
        filename: str,
        content: bytes,
        folder: str,
        content_type: str,
        file_size: int
    ) -> dict:
        """Save file to S3-compatible storage."""
        key = f"{folder}/{filename}"
        
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=content,
            ContentType=content_type
        )
        
        # Generate presigned URL valid for 7 days
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key},
            ExpiresIn=7 * 24 * 3600
        )
        
        return {
            "url": url,
            "filename": filename,
            "file_size": file_size,
            "file_type": content_type,
            "storage_type": "s3"
        }
    
    async def delete_file(self, url: str) -> bool:
        """Delete a file from storage."""
        if self.storage_type == "local":
            try:
                # Extract path from URL
                path_parts = url.split("/uploads/", 1)
                if len(path_parts) == 2:
                    file_path = self.local_storage_path / path_parts[1]
                    if file_path.exists():
                        file_path.unlink()
                        return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        else:
            try:
                # Extract key from URL
                key = url.split(f"{self.bucket_name}/", 1)[1].split("?")[0]
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
                return True
            except Exception as e:
                print(f"Error deleting file from S3: {e}")
                return False
        return False
    
    def validate_file(self, file: UploadFile) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded file.
        
        Returns:
            (is_valid, error_message)
        """
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if hasattr(file, 'size') and file.size is not None and file.size > max_size:
            return False, f"File size exceeds maximum allowed size of {max_size / (1024 * 1024)}MB"
        
        # Check file type
        allowed_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ]
        
        if file.content_type not in allowed_types:
            return False, f"File type {file.content_type} is not allowed"
        
        return True, None


# Singleton instance
storage_service = StorageService()
