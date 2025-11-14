# backend/app/api/uploads.py
"""File upload API endpoints for PS-2 evidence and attachments."""
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path

from app.models.complaint import Attachment, EvidenceType
from app.services.storage_service import storage_service
from app.services.auth import get_current_user
from app.models.user import UserDocument

router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_files(
    files: List[UploadFile] = File(...),
    evidence_type: EvidenceType = EvidenceType.OTHER,
    current_user: UserDocument = Depends(get_current_user)
):
    """
    Upload one or more evidence files.
    
    Supports multiple file uploads for complaint evidence.
    Files are validated and stored securely.
    
    Returns metadata for each uploaded file.
    """
    uploaded_files = []
    
    for file in files:
        # Validate file
        is_valid, error_message = storage_service.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Save file
        try:
            file_metadata = await storage_service.save_file(file, folder="evidence")
            
            # Create Attachment object
            attachment = Attachment(
                filename=file_metadata["filename"],
                file_type=file_metadata["file_type"],
                file_size=file_metadata["file_size"],
                url=file_metadata["url"],
                evidence_type=evidence_type
            )
            
            uploaded_files.append(attachment.dict())
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file {file.filename}: {str(e)}"
            )
    
    return {
        "status": "success",
        "files": uploaded_files,
        "count": len(uploaded_files)
    }


@router.get("/uploads/{folder}/{filename}")
async def serve_file(folder: str, filename: str):
    """
    Serve uploaded files from local storage.
    
    Only works with local storage. For S3, files are served via presigned URLs.
    """
    if storage_service.storage_type != "local":
        raise HTTPException(
            status_code=400,
            detail="File serving is only available for local storage. Use presigned URLs for S3."
        )
    
    file_path = storage_service.local_storage_path / folder / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    # Check if file is within allowed directory (security)
    try:
        file_path.resolve().relative_to(storage_service.local_storage_path.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(
        path=str(file_path),
        media_type="application/octet-stream",
        filename=filename
    )


@router.delete("/upload/{file_url:path}")
async def delete_file(
    file_url: str,
    current_user: UserDocument = Depends(get_current_user)
):
    """
    Delete an uploaded file.
    
    Requires authentication.
    """
    # Only admins can delete files
    if not current_user.is_admin():
        raise HTTPException(status_code=403, detail="Only admins can delete files")
    
    success = await storage_service.delete_file(file_url)
    
    if not success:
        raise HTTPException(status_code=404, detail="File not found or could not be deleted")
    
    return {"status": "success", "message": "File deleted successfully"}
