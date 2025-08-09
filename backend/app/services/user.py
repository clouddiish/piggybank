from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import UserEmailAlreadyExistsException, ActionForbiddenException
from app.core.config import get_settings
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import UserCreate, UserUpdate, UserFilters
from app.services.base import BaseService
from app.services.role import get_role_service


logger = get_logger(__name__)
settings = get_settings()


class UserService(BaseService[User, UserCreate, UserUpdate, UserFilters]):
    def __init__(self, session: AsyncSession) -> None:
        self.role_service = get_role_service(session=session)
        super().__init__(session=session, db_model_class=User, entity_type=EntityType.user)

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User | None: The User db model instance if found, None otherwise.

        """
        logger.info(f"executing query to fetch user with email {email}")

        query = await self.session.execute(select(User).where(User.email == email))
        entity = query.scalar_one_or_none()
        return entity

    async def _validate_create(self, create_schema: UserCreate) -> None:
        """
        Validate UserCreate schema.

        Args:
            schema (UserCreate): The schema to validate.

        Returns:
            None

        Raises:
            EntityNotFoundException: If the role with the given id does not exist.
            UserEmailAlreadyExists: If user with provided email already exists.
        """
        # verify role exists
        await self.role_service.get_by_id(entity_id=create_schema.role_id)

        # verify user with same email exists
        if await self.get_by_email(email=create_schema.email):
            raise UserEmailAlreadyExistsException(email=create_schema.email)

    async def _validate_update(self, entity_id: int, update_schema: UserUpdate) -> User:
        """
        Validate UserUpdate schema.

        Args:
            entity_id (int): The id of the user to validate.
            schema (UserUpdate): The schema to validate.

        Returns:
            User: The validated user.

        Raises:
            EntityNotFoundException: If the user or role with the given id do not exist.
            UserEmailAlreadyExists: If user with provided email already exists, and is not the same as the user being updated.
        """
        # verify user exists
        user_db = await self.get_by_id(entity_id=entity_id)

        # verify role exists
        await self.role_service.get_by_id(entity_id=update_schema.role_id)

        # verify user with same email exists, and is not the same as the user being updated
        existing = await self.get_by_email(email=update_schema.email)
        if existing and existing.id != user_db.id:
            raise UserEmailAlreadyExistsException(email=update_schema.email)

        return user_db

    async def _validate_delete(self, entity_id: int) -> User:
        """
        Validate deletion of a user.

        Args:
            entity_id (int): The id of the user to validate.

        Returns:
            User: The validated user.

        Raises:
            EntityNotFoundException: If the user with the given id does not exist.
            ActionForbiddenException: If trying to delete initial admin user.
        """
        # validate user exists
        user_db = await self.get_by_id(entity_id=entity_id)

        # disallow deleting initial admin
        if user_db.email == settings.initial_admin_email:
            raise ActionForbiddenException(detail="cannot delete initial admin user")

        return user_db


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
