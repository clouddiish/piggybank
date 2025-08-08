from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException, ActionForbiddenException
from app.core.logger import get_logger
from app.schemas import RoleCreate, RoleUpdate, RoleOut, RoleFilters
from app.services.role import RoleService, get_role_service


logger = get_logger(__name__)

router = APIRouter(prefix="/roles", tags=[Tag.role])


@router.get("/{role_id}", response_model=RoleOut, status_code=200, summary="get one role by its id")
async def get_role(role_id: int, service: RoleService = Depends(get_role_service)) -> RoleOut:
    logger.info(f"fetching role with id {role_id}")
    try:
        role = await service.get_by_id(entity_id=role_id)
        return role
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[RoleOut], status_code=200, summary="get all roles with optional filters")
async def get_roles(
    filters: Annotated[RoleFilters, Query()], service: RoleService = Depends(get_role_service)
) -> list[RoleOut]:
    logger.info(f"fetching all roles with filters {filters}")
    roles = await service.get_all_with_filters(filters=filters)
    logger.info(f"returned {len(roles)} roles")
    return roles


@router.post("", response_model=RoleOut, status_code=201, summary="create a new role")
async def create_role(new_role: RoleCreate, service: RoleService = Depends(get_role_service)) -> RoleOut:
    logger.info("creating a new role")
    role = await service.create(create_schema=new_role)
    return role


@router.put("/{role_id}", response_model=RoleOut, status_code=200, summary="update a role by its id")
async def update_role(
    role_id: int, updated_role: RoleUpdate, service: RoleService = Depends(get_role_service)
) -> RoleOut:
    logger.info(f"updating a role with id {role_id}")
    try:
        role = await service.update(entity_id=role_id, update_schema=updated_role)
        return role
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{role_id}", response_model=RoleOut, status_code=200, summary="delete a role by its id")
async def delete_role(role_id: int, service: RoleService = Depends(get_role_service)) -> RoleOut:
    logger.info(f"deleting a role with id {role_id}")
    try:
        role = await service.delete(entity_id=role_id)
        return role
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
