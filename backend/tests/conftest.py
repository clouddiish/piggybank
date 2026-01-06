from datetime import date
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.db_models
from app.main import app as fastapi_app
from app.common.enums import RoleName, TypeName
from app.core.config import get_settings
from app.core.seeder import seed_initial_data
from app.core.session import get_session
from app.db_models import User, Role, Type, Category, Transaction
from app.db_models.base import Base
from app.services import UserService, RoleService, TypeService, CategoryService, TransactionService


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


@pytest.fixture
async def admin_token(client_fixture: AsyncClient) -> str:
    """Fixture that returns a valid bearer token for the seeded admin."""
    payload = {"username": settings.initial_admin_email, "password": settings.initial_admin_password}
    response = await client_fixture.post("/token", data=payload)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
async def user_token(client_fixture: AsyncClient) -> str:
    """Fixture that creates and logs in a non-admin user."""
    # create non-admin user
    email = "test@email.com"
    password = "longpassword123"
    response = await client_fixture.post("/users", json={"email": email, "password": password})
    assert response.status_code == 201

    # get token
    response = await client_fixture.post("/token", data={"username": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def mock_role_service(mock_session: AsyncMock) -> RoleService:
    return RoleService(session=mock_session)


@pytest.fixture
def mock_roles() -> list[Role]:
    return [Role(id=i, name=role_name) for i, role_name in enumerate(RoleName)]


@pytest.fixture
def mock_user_service(mock_session: AsyncMock, mock_role_service: RoleService) -> UserService:
    return UserService(session=mock_session, role_service=mock_role_service)


@pytest.fixture
def mock_users() -> list[User]:
    return [
        User(id=1, role_id=1, email="test1@email.com", password_hash="hash1", is_protected=False),
        User(id=2, role_id=2, email="test2@email.com", password_hash="hash2", is_protected=True),
        User(id=3, role_id=2, email="test3@email.com", password_hash="hash3", is_protected=False),
    ]


@pytest.fixture
def mock_type_service(mock_session: AsyncMock) -> TypeService:
    return TypeService(session=mock_session)


@pytest.fixture
def mock_types() -> list[Type]:
    return [Type(id=i, name=type_name) for i, type_name in enumerate(TypeName)]


@pytest.fixture
def mock_category_service(
    mock_session: AsyncMock, mock_user_service: UserService, mock_type_service: TypeService
) -> CategoryService:
    return CategoryService(session=mock_session, user_service=mock_user_service, type_service=mock_type_service)


@pytest.fixture
def mock_categories() -> list[Category]:
    return [
        Category(id=1, user_id=1, type_id=1, name="salary"),
        Category(id=2, user_id=1, type_id=2, name="groceries"),
    ]


@pytest.fixture
def mock_transaction_service(
    mock_session: AsyncMock,
    mock_category_service: CategoryService,
    mock_type_service: TypeService,
    mock_user_service: UserService,
) -> TransactionService:
    return TransactionService(
        session=mock_session,
        category_service=mock_category_service,
        type_service=mock_type_service,
        user_service=mock_user_service,
    )


@pytest.fixture
def mock_transactions() -> list[Transaction]:
    return [
        Transaction(
            id=1, user_id=1, type_id=1, category_id=1, date=date(2025, 9, 1), value=10.5, comment="Test comment"
        ),
        Transaction(
            id=2, user_id=2, type_id=2, category_id=2, date=date(2025, 10, 1), value=101.5, comment="Test comment 2"
        ),
    ]
