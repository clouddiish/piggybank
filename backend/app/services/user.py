from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType, RoleName
from app.common.exceptions import UserEmailAlreadyExistsException, ActionForbiddenException
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import UserCreate, UserUpdate, UserFilters
from app.services.base import BaseService
from app.services.role import get_role_service


logger = get_logger(__name__)


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

    async def is_admin(self, user_id: int) -> bool:
        """
        Check if user has the admin role.

        Args:
            user_id (int): Id of the user to check.

        Returns:
            bool: True if user is an admin, False otherwise.

        Raises:
            EntityNotFoundException: If the user with provided id is not found.
        """
        user_db = await self.get_by_id(entity_id=user_id)
        admin_role = await self.role_service.get_by_name(role_name=RoleName.admin)
        if user_db.role_id == admin_role.id:
            return True
        return False

    async def _validate_create(self, create_schema: UserCreate, **kwargs) -> None:
        """
        Validate UserCreate schema.

        Args:
            schema (UserCreate): The schema to validate.
            kwargs: Additional arguments for creation.

        Returns:
            None

        Raises:
            UserEmailAlreadyExists: If user with provided email already exists.
        """
        # verify user with same email exists
        if await self.get_by_email(email=create_schema.email):
            raise UserEmailAlreadyExistsException(email=create_schema.email)

    async def _validate_update(self, entity_id: int, update_schema: UserUpdate, updated_by: User, **kwargs) -> User:
        """
        Validate UserUpdate schema.

        Args:
            entity_id (int): The id of the user to validate.
            schema (UserUpdate): The schema to validate.
            updated_by (User): The user doing the update.
            kwargs: Additional arguments for update.

        Returns:
            User: The validated user.

        Raises:
            EntityNotFoundException: If the user or role with the given id do not exist.
            UserEmailAlreadyExists: If user with provided email already exists, and is not the same as the user being updated.
            ActionForbiddenException: If the user doing the update is not allowed to perform the update.
        """
        # verify user exists
        user_db = await self.get_by_id(entity_id=entity_id)

        # verify if they can update at all
        if not (updated_by.id == user_db.id or await self.is_admin(user_id=updated_by.id)):
            raise ActionForbiddenException(detail="only admins can update other users")

        # verify role exists
        await self.role_service.get_by_id(entity_id=update_schema.role_id)

        # verify if they can update roles
        if user_db.is_protected and user_db.role_id != update_schema.role_id:
            raise ActionForbiddenException(detail="cannot update role of protected user")
        if not await self.is_admin(user_id=updated_by.id) and user_db.role_id != update_schema.role_id:
            raise ActionForbiddenException(detail="only admins can update role of users")

        # verify user with same email exists, and is not the same as the user being updated
        existing = await self.get_by_email(email=update_schema.email)
        if existing and existing.id != user_db.id:
            raise UserEmailAlreadyExistsException(email=update_schema.email)

        return user_db

    async def _validate_delete(self, entity_id: int, deleted_by: User, **kwargs) -> User:
        """
        Validate deletion of a user.

        Args:
            entity_id (int): The id of the user to validate.
            deleted_by (User): The user doing the delete.
            kwargs: Additional arguments for deletion.

        Returns:
            User: The validated user.

        Raises:
            EntityNotFoundException: If the user with the given id does not exist.
            ActionForbiddenException: If trying to delete initial admin user, or if user doing the delete is not allowed to perform the delete.
        """
        # verify user exists
        user_db = await self.get_by_id(entity_id=entity_id)

        # verify they can delete
        if not (deleted_by.id == user_db.id or await self.is_admin(user_id=deleted_by.id)):
            raise ActionForbiddenException(detail="only admins can delete other users")

        # disallow deleting initial admin
        if user_db.is_protected:
            raise ActionForbiddenException(detail="cannot delete protected user")

        return user_db


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session=session)
