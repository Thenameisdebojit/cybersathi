# backend/app/services/auth.py
"""Authentication and authorization service."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.models.user import UserDocument, UserRole, UserStatus
from app.models.audit_log import AuditLogDocument, AuditAction

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()


class AuthService:
    """Authentication service for user management and JWT tokens."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        user_id: str,
        email: str,
        role: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "sub": user_id,
            "email": email,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        """Create a refresh token."""
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire,
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and verify a JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[UserDocument]:
        """Authenticate a user by email and password."""
        user = await UserDocument.find_one(UserDocument.email == email)
        
        if not user:
            return None
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account is locked until {user.locked_until}"
            )
        
        # Check if account is active
        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account is {user.status.value}"
            )
        
        # Verify password
        if not AuthService.verify_password(password, user.hashed_password):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(hours=1)
            
            await user.save()
            
            # Log failed login
            await AuditLogDocument.log(
                action=AuditAction.LOGIN_FAILED,
                resource_type="user",
                user_email=email,
                resource_id=str(user.id),
            )
            
            return None
        
        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        await user.save()
        
        # Log successful login
        await AuditLogDocument.log(
            action=AuditAction.USER_LOGIN,
            resource_type="user",
            user_id=str(user.id),
            user_email=user.email,
            resource_id=str(user.id),
        )
        
        return user
    
    @staticmethod
    async def create_user(
        email: str,
        password: Optional[str],
        full_name: str,
        phone: Optional[str] = None,
        role: UserRole = UserRole.VIEWER,
        department: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> UserDocument:
        """Create a new user."""
        import json
        from datetime import datetime
        
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,B","location":"auth.py:142","message":"create_user entry","data":{"email":email,"has_password":bool(password),"full_name":full_name},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        try:
            # Check if user already exists
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"auth.py:154","message":"before find_one check","data":{"email":email},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            existing_user = await UserDocument.find_one(UserDocument.email == email)
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"auth.py:155","message":"after find_one check","data":{"existing_user_found":existing_user is not None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            # Hash password if provided (for local registration)
            hashed_password = None
            if password:
                if len(password) < settings.MIN_PASSWORD_LENGTH:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
                    )
                hashed_password = AuthService.hash_password(password)
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"auth.py:172","message":"before UserDocument creation","data":{"has_hashed_password":hashed_password is not None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            # Create user
            user = UserDocument(
                email=email,
                phone=phone,
                hashed_password=hashed_password,
                full_name=full_name,
                role=role,
                department=department,
                created_by=created_by,
                provider="local",  # Explicitly set provider for local registration
                status=UserStatus.ACTIVE,  # Explicitly set status
            )
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"auth.py:182","message":"after UserDocument creation","data":{"user_created":True,"has_id":hasattr(user,'id')},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            # Insert user into database
            try:
                # #region agent log
                try:
                    from app.database import db
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"auth.py:186","message":"before insert call","data":{"using_mock":db.using_mock if hasattr(db,'using_mock') else None,"has_client":db.client is not None if hasattr(db,'client') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                await user.insert()
                
                # #region agent log
                try:
                    # Verify user was actually saved by querying it back
                    from app.database import db
                    # UserDocument is already imported at top of file
                    saved_user = await UserDocument.find_one(UserDocument.email == email)
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"auth.py:187","message":"after insert success","data":{"user_id":str(user.id) if hasattr(user,'id') else None,"saved_user_found":saved_user is not None,"saved_user_id":str(saved_user.id) if saved_user and hasattr(saved_user,'id') else None,"using_mock":db.using_mock if hasattr(db,'using_mock') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
            except Exception as insert_error:
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"auth.py:188","message":"insert error caught","data":{"error_type":type(insert_error).__name__,"error_msg":str(insert_error)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                error_msg = str(insert_error)
                # Check for duplicate email error
                if "duplicate" in error_msg.lower() or "E11000" in error_msg:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User with this email already exists"
                    )
                # Re-raise with more context
                raise Exception(f"Failed to insert user into database: {error_msg}") from insert_error
            
            # Log user creation (non-blocking - don't fail registration if audit log fails)
            try:
                await AuditLogDocument.log(
                    action=AuditAction.USER_CREATED,
                    resource_type="user",
                    user_id=created_by,
                    resource_id=str(user.id),
                    description=f"Created user: {email}",
                )
            except Exception as log_error:
                # Log the error but don't fail user creation
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to create audit log for user creation: {log_error}")
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,B","location":"auth.py:213","message":"create_user returning","data":{"user_id":str(user.id) if hasattr(user,'id') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            return user
        except HTTPException:
            raise
        except Exception as e:
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"auth.py:217","message":"exception in create_user","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            error_msg = str(e)
            if "ServerSelectionTimeoutError" in error_msg or "Connection" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database is not connected. Please configure MongoDB Atlas connection string in backend/.env (MONGODB_URL). Get free MongoDB Atlas at: https://www.mongodb.com/cloud/atlas"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {error_msg}"
            )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserDocument:
    """Dependency to get current authenticated user."""
    token = credentials.credentials
    
    try:
        payload = AuthService.decode_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = await UserDocument.get(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.status.value}"
        )
    
    return user


async def get_current_admin_user(
    current_user: UserDocument = Depends(get_current_user)
) -> UserDocument:
    """Dependency to ensure current user is an admin."""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_role(*required_roles: UserRole):
    """Decorator to require specific roles."""
    async def role_checker(current_user: UserDocument = Depends(get_current_user)) -> UserDocument:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join([r.value for r in required_roles])}"
            )
        return current_user
    return role_checker
