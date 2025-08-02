from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import EntityNotFoundException
from app.core.config import get_settings
from app.core.logger import logger
from app.db_models import User, Role
from app.services.security import get_password_hash


async def seed_initial_data(session: AsyncSession) -> None:
    settings = get_settings()

    logger.debug("creating initial roles")
    for role_name in settings.initial_roles:
        result = await session.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if not role:
            new_role = Role(name=role_name)
            session.add(new_role)
            await session.flush()
            logger.info(f"created {role_name} role")
        else:
            logger.info(f"{role_name} role already exists")

    logger.debug("creating initial admin user")
    result = await session.execute(select(User).where(User.email == settings.initial_admin_email))
    user = result.scalar_one_or_none()
    if not user:
        result = await session.execute(select(Role.id).where(Role.name == settings.initial_admin_role))
        admin_role_id = result.scalar_one_or_none()
        if not admin_role_id:
            logger.error(f"failed seeding initial data")
            raise EntityNotFoundException(entity_id=settings.initial_admin_role, entity_type=EntityType.role)
        new_user = User(
            role_id=admin_role_id,
            email=settings.initial_admin_email,
            password_hash=get_password_hash(settings.initial_admin_password),
        )
        session.add(new_user)
        await session.flush()
        logger.info(f"created initial admin user with email {settings.initial_admin_email}")
    else:
        logger.info(f"user with email {settings.initial_admin_email} already exists")

    await session.commit()
