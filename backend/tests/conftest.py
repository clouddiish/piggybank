from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app as fastapi_app
from app.core.config import get_settings
from app.core.seeder import seed_initial_data
from app.core.session import get_session
from app.db_models.base import Base
import app.db_models


settings = get_settings()

test_engine = create_async_engine(
    settings.test_database_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def mock_session() -> AsyncMock:
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture()
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_async_session() as session:
        await seed_initial_data(session)
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def client_fixture(session_fixture: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
        yield session_fixture

    fastapi_app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client

    fastapi_app.dependency_overrides.clear()
