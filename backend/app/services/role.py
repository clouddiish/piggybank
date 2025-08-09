from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import ActionForbiddenException
from app.core.config import get_settings
from app.core.logger import get_logger
from app.core.session import get_session
from app.db_models import Role
from app.schemas import RoleCreate, RoleUpdate, RoleFilters
from app.services.base import BaseService


logger = get_logger(__name__)
settings = get_settings()


class RoleService(BaseService[Role, RoleCreate, RoleUpdate, RoleFilters]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, db_model_class=Role, entity_type=EntityType.role)

    async def _validate_delete(self, entity_id: int) -> Role:
        """
        Validate deletion of a role.

        Args:
            entity_id (int): The id of the role to validate.

        Returns:
            Role: The validated role.

        Raises:
            EntityNotFoundException: If the role with the given id does not exist.
            ActionForbiddenException: If trying to delete initial admin role.
        """
        # validate role exists
        role_db = await self.get_by_id(entity_id=entity_id)

        # disallow deleting initial admin role
        if role_db.name == settings.initial_admin_role:
            raise ActionForbiddenException(detail="cannot delete initial admin role")

        return role_db


def get_role_service(session: AsyncSession = Depends(get_session)) -> RoleService:
    return RoleService(session)
