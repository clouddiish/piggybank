from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.common.enums import RoleName
from app.core.config import get_settings
from app.db_models import User
from app.schemas import TokenData
from app.services.user import UserService, get_user_service


settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str, user_service: UserService) -> User | bool:
    user_db = await user_service.get_by_email(email=email)
    if not user_db:
        return False
    if not verify_password(plain_password=password, hashed_password=user_db.password_hash):
        return False
    return user_db


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    credentials_exception = HTTPException(
        status_code=401, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user_db = await user_service.get_by_email(email=token_data.username)
    if user_db is None:
        raise credentials_exception
    return user_db


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    current_user_role = await user_service.role_service.get_by_id(entity_id=current_user.role_id)
    if not current_user_role.name.value == RoleName.admin.value:
        raise HTTPException(status_code=403, detail="user is not an admin")
    return current_user
