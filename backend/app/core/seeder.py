from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType, RoleName
from app.common.exceptions import EntityNotFoundException
from app.core.config import get_settings
from app.core.logger import get_logger
from app.db_models import User, Role
from app.services.security import get_password_hash


async def seed_initial_data(session: AsyncSession) -> None:
    settings = get_settings()
    logger = get_logger(__name__)

    logger.debug("creating initial roles")
    for role_enum in RoleName:
        result = await session.execute(select(Role).where(Role.name == role_enum.value))
        role = result.scalar_one_or_none()
        if not role:
            new_role = Role(name=role_enum)
            session.add(new_role)
            await session.flush()
            logger.info(f"created {role_enum.value} role")
        else:
            logger.info(f"{role_enum.value} role already exists")

    logger.debug("creating initial admin user")
    result = await session.execute(select(User).where(User.email == settings.initial_admin_email))
    user = result.scalar_one_or_none()
    if not user:
        result = await session.execute(select(Role.id).where(Role.name == RoleName.admin.value))
        admin_role_id = result.scalar_one_or_none()
        if not admin_role_id:
            logger.error(f"failed seeding initial data")
            raise EntityNotFoundException(entity_id=RoleName.admin.value, entity_type=EntityType.role)
        new_user = User(
            role_id=admin_role_id,
            email=settings.initial_admin_email,
            password_hash=get_password_hash(settings.initial_admin_password),
            is_protected=True,
        )
        session.add(new_user)
        await session.flush()
        logger.info(f"created initial admin user with email {settings.initial_admin_email}")
    else:
        logger.info(f"user with email {settings.initial_admin_email} already exists")

    await session.commit()
