from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.common.enums import Tag
from app.common.responses import common_responses_dict
from app.core.config import get_settings
from app.schemas import Token
from app.services import UserService, get_user_service
from app.services.security import authenticate_user, create_access_token


settings = get_settings()
router = APIRouter(prefix="/token", tags=[Tag.security])


@router.post("", responses=common_responses_dict)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserService = Depends(get_user_service)
):
    user_db = await authenticate_user(email=form_data.username, password=form_data.password, user_service=user_service)
    if not user_db:
        raise HTTPException(
            status_code=401, detail="incorrect username or password", headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user_db.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
