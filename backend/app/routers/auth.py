# backend/app/routers/auth.py
"""Authentication router for user login, registration, and profile management."""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from datetime import timedelta, datetime
import httpx
from pydantic import ValidationError

try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False

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
    import logging
    import json
    import os
    from datetime import datetime
    logger = logging.getLogger(__name__)
    
    # #region agent log
    try:
        import os
        log_path = r'd:\cybersathi\.cursor\debug.log'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,B,C,D,E","location":"auth.py:30","message":"register endpoint entry","data":{"email":user_data.email,"has_password":bool(user_data.password),"full_name":user_data.full_name,"phone":user_data.phone},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
    except Exception as log_err:
        logger.error(f"Failed to write debug log: {log_err}")
    # #endregion
    
    try:
        # Validate password for local registration (not OAuth)
        if user_data.provider == "local" or user_data.provider is None:
            if not user_data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password is required for registration"
                )
            if len(user_data.password) < settings.MIN_PASSWORD_LENGTH:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
                )
        
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,B","location":"auth.py:57","message":"before create_user call","data":{"email":user_data.email},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        logger.info(f"Attempting to create user: {user_data.email}")
        user = await AuthService.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            department=user_data.department,
        )
        
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,B","location":"auth.py:67","message":"after create_user call","data":{"user_id":str(user.id) if hasattr(user,'id') else None,"has_id":hasattr(user,'id')},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        logger.info(f"User created successfully: {user.id}")
        
        # Convert to response model using Pydantic's model_validate
        try:
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C,E","location":"auth.py:71","message":"before to_dict call","data":{"user_id":str(user.id) if hasattr(user,'id') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            user_dict = user.to_dict()
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C,E","location":"auth.py:73","message":"after to_dict call","data":{"user_dict_keys":list(user_dict.keys()) if user_dict else None,"has_id":'id' in user_dict if user_dict else False},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            # Use model_validate for better error handling
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"auth.py:74","message":"before model_validate call","data":{"user_dict_keys":list(user_dict.keys()) if user_dict else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            response = UserResponse.model_validate(user_dict)
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"auth.py:75","message":"after model_validate success","data":{"response_id":response.id if hasattr(response,'id') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            return response
        except Exception as conv_error:
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"auth.py:76","message":"conversion error caught","data":{"error_type":type(conv_error).__name__,"error_msg":str(conv_error)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            logger.error(f"Error converting user to response: {conv_error}")
            logger.error(f"User data: {user.to_dict()}")
            # Fallback: try direct conversion
            try:
                return UserResponse(
                    id=str(user.id),
                    email=user.email,
                    phone=user.phone,
                    full_name=user.full_name,
                    role=user.role,
                    status=user.status,
                    department=user.department,
                    last_login=user.last_login,
                    created_at=user.created_at,
                    provider=user.provider,
                    profile_picture=user.profile_picture,
                )
            except Exception as fallback_error:
                logger.error(f"Fallback conversion also failed: {fallback_error}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create response: {str(conv_error)}"
                )
        
    except HTTPException:
        raise
    except ValidationError as e:
        # Handle Pydantic validation errors
        error_details = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            error_details.append(f"{field}: {error['msg']}")
        logger.error(f"Validation error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error: " + "; ".join(error_details)
        )
    except Exception as e:
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"auth.py:100","message":"exception caught in register","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        error_msg = str(e)
        logger.error(f"Registration error: {error_msg}", exc_info=True)
        # Provide more helpful error messages
        if "duplicate key" in error_msg.lower() or "already exists" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {error_msg}"
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
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
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


@router.get("/google/login")
async def google_login():
    """
    Redirect to Google OAuth login page.
    """
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_REDIRECT_URI:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured. Please add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REDIRECT_URI to backend/.env"
        )
    
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline"
    )
    return {"url": google_auth_url}


@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(code: str):
    """
    Handle Google OAuth callback and create/login user.
    
    - **code**: Authorization code from Google
    """
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange code for token"
                )
            
            tokens = token_response.json()
            id_token_str = tokens.get("id_token")
            
            # Verify and decode ID token
            if not GOOGLE_AUTH_AVAILABLE:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Google authentication libraries not available"
                )
            
            idinfo = id_token.verify_oauth2_token(
                id_token_str, 
                google_requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            # Extract user info
            google_id = idinfo.get("sub")
            email = idinfo.get("email")
            name = idinfo.get("name")
            picture = idinfo.get("picture")
            
            # Check if user exists
            user = await UserDocument.find_one(
                {"$or": [
                    {"provider_id": google_id, "provider": "google"},
                    {"email": email}
                ]}
            )
            
            if user:
                # Update existing user
                user.provider = "google"
                user.provider_id = google_id
                user.profile_picture = picture
                user.last_login = datetime.utcnow()
                await user.save()
            else:
                # Create new user
                user = UserDocument(
                    email=email,
                    phone="",  # Will be updated later
                    full_name=name,
                    provider="google",
                    provider_id=google_id,
                    profile_picture=picture,
                    role=UserRole.VIEWER,
                    status=UserStatus.ACTIVE,
                    last_login=datetime.utcnow(),
                )
                await user.insert()
                
                await AuditLogDocument.log(
                    action=AuditAction.USER_CREATED,
                    resource_type="user",
                    user_id=str(user.id),
                    user_email=user.email,
                    resource_id=str(user.id),
                    description="User registered via Google OAuth",
                )
            
            # Create tokens
            access_token = AuthService.create_access_token(
                user_id=str(user.id),
                email=user.email,
                role=user.role.value,
            )
            
            refresh_token = AuthService.create_refresh_token(user_id=str(user.id))
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user=UserResponse(**user.to_dict())
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication failed: {str(e)}"
        )
