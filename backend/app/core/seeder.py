from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import RoleNotFoundException
from app.core.config import get_settings
from app.core.logger import logger
from app.core.security import get_password_hash
from app.db_models import User, Role


async def seed_initial_data(session: AsyncSession) -> None:
    settings = get_settings()

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

    result = await session.execute(select(User).where(User.email == settings.initial_admin_email))
    user = result.scalar_one_or_none()
    if not user:
        result = await session.execute(select(Role.id).where(Role.name == "admin"))
        admin_role_id = result.scalar_one_or_none()
        if not admin_role_id:
            logger.error(f"failed seeding initial data")
            raise RoleNotFoundException("admin role not found")
        new_user = User(
            role_id=admin_role_id,
            email=settings.initial_admin_email,
            password_hash=get_password_hash(settings.initial_admin_password),
        )
        session.add(new_user)
        await session.flush()
        logger.info(f"created initial admin user with emain {settings.initial_admin_email}")
    else:
        logger.info(f"user with email {settings.initial_admin_email} already exists")

    await session.commit()
