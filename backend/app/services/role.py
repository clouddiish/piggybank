from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType, RoleName
from app.common.exceptions import EntityNotFoundException
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

    async def get_by_name(self, role_name: RoleName) -> Role:
        """
        Get role by name.

        Args:
            role_name (RoleName): The name of the role to retrieve.

        Returns:
            Role: The selected role.

        Raises:
            EntityNotFoundException: If the role with given name was not found.
        """
        logger.info(f"executing query to fetch role with name {role_name.value}")

        query = await self.session.execute(select(Role).where(Role.name == role_name))
        role = query.scalar_one_or_none()

        if not role:
            logger.error(f"role with name {role_name.value} not found")
            raise EntityNotFoundException(entity_id=role_name, entity_type=EntityType.role)

        return role


def get_role_service(session: AsyncSession = Depends(get_session)) -> RoleService:
    return RoleService(session)
