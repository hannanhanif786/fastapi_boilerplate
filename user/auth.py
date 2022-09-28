from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .db import get_db
from .schemas import TokenData, CreateUserIn
from sqlalchemy.orm import Session
from .query import user_get_by_email
from pydantic import ValidationError
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = "HS256"


def get_password_hash(password):
    """convert plain to hash password

    Args:
        password (_type_): password

    Returns:
        _type_: hashed password
    """

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """verify password

    Args:
        plain_password (_type_): password without hashed
        hashed_password (bool): hased password

    Returns:
        _type_: verification detail
    """

    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    """for authentication

    Args:
        username (str): username
        password (str): password
        db (Session): database connection

    Returns:
        _type_: authenticated user if conditions true
    """

    user = user_get_by_email(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """create acces token

    Args:
        data (dict): data
        expires_delta (Union[timedelta, None], optional): time . Defaults to None.

    Returns:
        _type_: token
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """get current user after authorization

    Args:
        token (str, optional): token
        db (Session, optional): database connection

    Raises:
        HTTPException: 401, Could not validate credentials
    Returns:
        _type_: user obj
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = user_get_by_email(username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: CreateUserIn = Depends(get_current_user),
):
    """for checking active user

    Args:
        current_user (AddUser, optional): for checking scope

    Raises:
        HTTPException: 400, not active

    Returns:
        _type_: current_user
    """

    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
