from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.core.logger import get_logger
from app.core.session import get_session
from app.db_models import Role
from app.schemas import RoleCreate, RoleUpdate, RoleFilters
from app.services import BaseService


logger = get_logger(__name__)


class RoleService(BaseService[Role, RoleCreate, RoleUpdate, RoleFilters]):
    # has available all the methods from BaseService, but only gets are exposed in routes
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, db_model_class=Role, entity_type=EntityType.role)


def get_role_service(session: AsyncSession = Depends(get_session)) -> RoleService:
    return RoleService(session)
