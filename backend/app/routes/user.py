from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag, RoleName
from app.common.exceptions import EntityNotFoundException, UserEmailAlreadyExistsException, ActionForbiddenException
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import UserCreate, UserUpdate, UserOut, UserFilters
from app.services import UserService, get_user_service
from app.services.security import get_password_hash, get_current_user, get_current_admin


logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=[Tag.user])


@router.get("/me", response_model=UserOut, status_code=200, summary="get information about the current user")
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut, status_code=200, summary="get one user by their id")
async def get_user(
    user_id: int, service: UserService = Depends(get_user_service), current_admin: User = Depends(get_current_admin)
) -> UserOut:
    logger.info(f"fetching user with id {user_id}")
    try:
        user = await service.get_by_id(entity_id=user_id)
        return user
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[UserOut], status_code=200, summary="get all users with optional filters")
async def get_users(
    filters: Annotated[UserFilters, Query()],
    service: UserService = Depends(get_user_service),
    current_admin: User = Depends(get_current_admin),
) -> list[UserOut]:
    logger.info(f"fetching all users with filters {filters}")
    users = await service.get_all_with_filters(filters=filters)
    logger.info(f"returned {len(users)} users")
    return users


@router.post("", response_model=UserOut, status_code=201, summary="create a new user")
async def create_user(new_user: UserCreate, service: UserService = Depends(get_user_service)) -> UserOut:
    logger.info("creating a new user")
    try:
        # find id of user role
        user_role = await service.role_service.get_by_name(role_name=RoleName.user)
        # create new user with base user role
        user = await service.create(
            create_schema=new_user, password_hash=get_password_hash(new_user.password), role_id=user_role.id
        )
        return user
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/{user_id}", response_model=UserOut, status_code=200, summary="update a user by their id")
async def update_user(
    user_id: int,
    updated_user: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> UserOut:
    logger.info(f"updating a user with id {user_id}")
    try:
        user = await service.update(
            entity_id=user_id,
            update_schema=updated_user,
            password_hash=get_password_hash(updated_user.password),
            updated_by=current_user,
        )
        return user
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{user_id}", response_model=UserOut, status_code=200, summary="delete a user by their id")
async def delete_user(
    user_id: int, service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)
) -> UserOut:
    logger.info(f"deleting a user with id {user_id}")
    try:
        user = await service.delete(entity_id=user_id, deleted_by=current_user)
        return user
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
