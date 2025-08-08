from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import UserEmailAlreadyExists
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import UserCreate, UserUpdate, UserFilters
from app.services.base import BaseService
from app.services.role import get_role_service
from app.services.security import get_password_hash


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

    async def create(self, create_schema: UserCreate) -> User:
        """
        Create new user in the database.

        Args:
            create_schema (UserCreate): The schema for creating the user.

        Returns:
            User: The created user.

        Raises:
            EntityNotFoundException: If the role with the given role_id does not exist.
            UserEmailAlreadyExists: If user with provided email already exists.
        """
        logger.info(f"executing query to create a new user")

        # verify role exists
        await self.role_service.get_by_id(entity_id=create_schema.role_id)

        # verify user with same email exists
        if await self.get_by_email(email=create_schema.email):
            raise UserEmailAlreadyExists(email=create_schema.email)

        user_db = User(
            role_id=create_schema.role_id,
            email=create_schema.email,
            password_hash=get_password_hash(create_schema.password),
        )
        self.session.add(user_db)
        await self.session.commit()
        return user_db

    async def update(self, entity_id: int, update_schema: UserUpdate) -> User:
        """
        Update an existing user in the database.

        Args:
            entity_id (int): The id of the user to update.
            update_schema (UserUpdate): The schema for updating the user.

        Returns:
            User: The updated user.

        Raises:
            EntityNotFoundException: If the user with the given id or the provided role_id do not exist.
        """
        logger.info(f"executing query to update user with id {entity_id}")

        user_db = await self.get_by_id(entity_id=entity_id)

        # verify role exists
        await self.role_service.get_by_id(entity_id=update_schema.role_id)

        # verify user with same email exists
        if await self.get_by_email(email=update_schema.email):
            raise UserEmailAlreadyExists(email=update_schema.email)

        user_db.role_id = update_schema.role_id
        user_db.email = update_schema.email
        user_db.password_hash = get_password_hash(update_schema.password)

        self.session.add(user_db)
        await self.session.commit()
        await self.session.refresh(user_db)
        return user_db


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
