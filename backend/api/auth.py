import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models.user import User
from schemas.auth import UserCreate, UserLogin, Token
from utils.security import verify_password, get_password_hash
from utils.auth import create_access_token
from utils.validation import validate_email, validate_password
from utils.logging import get_logger
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

from middleware.auth import get_current_user

router = APIRouter()
logger = get_logger(__name__)

@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    logger.info(f"User registration attempt for email: {user.email}")

    # Validate email format
    if not validate_email(user.email):
        logger.warning(f"Invalid email format attempted: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    if not validate_password(user.password):
        logger.warning(f"Password validation failed for user: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        )

    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        logger.warning(f"Registration attempted for existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    logger.info(f"User registered successfully: {db_user.id}")

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user and return an access token.
    """
    logger.info(f"Login attempt for email: {user_credentials.email}")

    # Find user by email
    user = session.exec(select(User).where(User.email == user_credentials.email)).first()
    if not user:
        logger.warning(f"Login failed: User not found for email: {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(user_credentials.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid password for email: {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"User logged in successfully: {user.id}")

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's profile information.
    """
    logger.info(f"Profile requested for user: {current_user.id}")
    return current_user