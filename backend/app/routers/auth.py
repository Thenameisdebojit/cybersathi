# backend/app/routers/auth.py
"""Authentication router for user login, registration, and profile management."""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta

from app.models.user import (
    UserCreate, UserLogin, UserResponse, TokenResponse, 
    UserDocument, UserRole, UserStatus
)
from app.models.audit_log import AuditLogDocument, AuditAction
from app.services.auth import AuthService, get_current_user, get_current_admin_user
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **password**: Min 8 characters
    - **full_name**: User's full name
    - **phone**: Contact number
    - **role**: User role (default: viewer)
    """
    try:
        user = await AuthService.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            department=user_data.department,
        )
        
        return UserResponse(**user.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT tokens.
    
    - **email**: User's email
    - **password**: User's password
    
    Returns access token, refresh token, and user information.
    """
    user = await AuthService.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = AuthService.create_access_token(
        user_id=str(user.id),
        email=user.email,
        role=user.role.value,
    )
    
    # Create refresh token
    refresh_token = AuthService.create_refresh_token(user_id=str(user.id))
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(**user.to_dict())
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    try:
        payload = AuthService.decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = await UserDocument.get(user_id)
        
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token = AuthService.create_access_token(
            user_id=str(user.id),
            email=user.email,
            role=user.role.value,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(**user.to_dict())
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserDocument = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Requires valid JWT token in Authorization header.
    """
    return UserResponse(**current_user.to_dict())


@router.post("/logout")
async def logout(current_user: UserDocument = Depends(get_current_user)):
    """
    Logout current user (client should discard tokens).
    
    Note: JWT tokens are stateless, so actual logout is handled client-side.
    This endpoint logs the logout event for audit purposes.
    """
    await AuditLogDocument.log(
        action=AuditAction.USER_LOGOUT,
        resource_type="user",
        user_id=str(current_user.id),
        user_email=current_user.email,
        resource_id=str(current_user.id),
    )
    
    return {"message": "Successfully logged out"}


@router.put("/me", response_model=UserResponse)
async def update_profile(
    full_name: str = None,
    phone: str = None,
    current_user: UserDocument = Depends(get_current_user)
):
    """
    Update current user's profile information.
    
    - **full_name**: New full name (optional)
    - **phone**: New phone number (optional)
    """
    if full_name:
        current_user.full_name = full_name
    if phone:
        current_user.phone = phone
    
    await current_user.save()
    
    await AuditLogDocument.log(
        action=AuditAction.USER_UPDATED,
        resource_type="user",
        user_id=str(current_user.id),
        user_email=current_user.email,
        resource_id=str(current_user.id),
        description="Profile updated",
    )
    
    return UserResponse(**current_user.to_dict())


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserDocument = Depends(get_current_user)
):
    """
    Change current user's password.
    
    - **current_password**: Current password for verification
    - **new_password**: New password (min 8 characters)
    """
    # Verify current password
    if not AuthService.verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password
    if len(new_password) < settings.MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
        )
    
    # Update password
    current_user.hashed_password = AuthService.hash_password(new_password)
    await current_user.save()
    
    # Log password change
    await AuditLogDocument.log(
        action=AuditAction.PASSWORD_CHANGED,
        resource_type="user",
        user_id=str(current_user.id),
        user_email=current_user.email,
        resource_id=str(current_user.id),
    )
    
    return {"message": "Password changed successfully"}
