from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from unittest.mock import AsyncMock, patch

from app.common.enums import RoleName
from app.db_models import User, Role
from app.services import UserService, RoleService
from app.services.security import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_admin,
)


@pytest.mark.unit
class TestSecurityServices:
    @pytest.mark.anyio
    async def test_verify_password__returns_True(self):
        password = "secret123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.anyio
    async def test_verify_password__returns_False(self):
        password = "secret123"
        wrong_password = "wrong123"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    @pytest.mark.anyio
    async def test_verify_password__invalid_hash(self):
        with pytest.raises(ValueError):
            verify_password("test", "not_a_valid_hash")

    @pytest.mark.anyio
    async def test_get_password_hash__returns_hash(self):
        password = "secret123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert hashed != password
        assert hashed.startswith("$2b$")

    @pytest.mark.anyio
    async def test_authenticate_user__success(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[0])

        with patch("app.services.security.verify_password", return_value=True):
            user = await authenticate_user(
                email=mock_users[0].email, password="password", user_service=mock_user_service
            )

        mock_user_service.get_by_email.assert_awaited_once_with(email=mock_users[0].email)
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_authenticate_user__not_found(self, mock_user_service: UserService) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user = await authenticate_user(email="missing@email.com", password="password", user_service=mock_user_service)

        mock_user_service.get_by_email.assert_awaited_once_with(email="missing@email.com")
        assert user is False

    @pytest.mark.anyio
    async def test_authenticate_user__wrong_password(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[0])

        with patch("app.services.security.verify_password", return_value=False):
            user = await authenticate_user(
                email=mock_users[0].email, password="wrongpass", user_service=mock_user_service
            )

        mock_user_service.get_by_email.assert_awaited_once_with(email=mock_users[0].email)
        assert user is False

    @pytest.mark.anyio
    async def test_create_access_token__with_expiry(self) -> None:
        data = {"sub": "user1"}
        expires = timedelta(minutes=30)

        with patch("app.services.security.jwt.encode", return_value="token123") as mock_encode:
            token = create_access_token(data, expires)

        mock_encode.assert_called_once()
        args, _ = mock_encode.call_args
        assert "exp" in args[0]
        assert isinstance(args[0]["exp"], datetime)
        assert token == "token123"

    @pytest.mark.anyio
    async def test_create_access_token__default_expiry(self) -> None:
        data = {"sub": "user1"}

        with patch("app.services.security.jwt.encode", return_value="token123") as mock_encode:
            token = create_access_token(data)

        mock_encode.assert_called_once()
        args, _ = mock_encode.call_args
        exp_time = args[0]["exp"]
        assert abs(exp_time - (datetime.now(timezone.utc) + timedelta(minutes=15))) < timedelta(seconds=5)
        assert token == "token123"

    @pytest.mark.anyio
    async def test_get_current_user__success(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        token_data = {"sub": mock_users[0].email}
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[0])

        with patch("app.services.security.jwt.decode", return_value=token_data):
            user = await get_current_user("token", mock_user_service)

        mock_user_service.get_by_email.assert_awaited_once_with(email=mock_users[0].email)
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_get_current_user__invalid_token(self, mock_user_service: UserService) -> None:
        with patch("app.services.security.jwt.decode", side_effect=InvalidTokenError):
            with pytest.raises(HTTPException) as e:
                await get_current_user("badtoken", mock_user_service)
        assert e.value.status_code == 401

    @pytest.mark.anyio
    async def test_get_current_user__no_username(self, mock_user_service: UserService) -> None:
        with patch("app.services.security.jwt.decode", return_value={}):
            with pytest.raises(HTTPException) as e:
                await get_current_user("token", mock_user_service)
        assert e.value.status_code == 401

    @pytest.mark.anyio
    async def test_get_current_user__user_not_found(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        with patch("app.services.security.jwt.decode", return_value={"sub": mock_users[0].email}):
            with pytest.raises(HTTPException) as e:
                await get_current_user("token", mock_user_service)
        assert e.value.status_code == 401

    @pytest.mark.anyio
    async def test_get_current_admin__success(
        self,
        mock_user_service: UserService,
        mock_users: list[User],
        mock_role_service: RoleService,
        mock_roles: list[Role],
    ) -> None:
        admin_role = next(role for role in mock_roles if role.name.value == RoleName.admin.value)
        mock_user_service.role_service = mock_role_service
        mock_role_service.get_by_id = AsyncMock(return_value=admin_role)

        user = await get_current_admin(mock_users[0], mock_user_service)

        mock_role_service.get_by_id.assert_awaited_once_with(entity_id=mock_users[0].role_id)
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_get_current_admin__not_admin(
        self,
        mock_user_service: UserService,
        mock_users: list[User],
        mock_role_service: RoleService,
        mock_roles: list[Role],
    ) -> None:
        non_admin_role = next(role for role in mock_roles if role.name.value != RoleName.admin.value)
        mock_user_service.role_service = mock_role_service
        mock_role_service.get_by_id = AsyncMock(return_value=non_admin_role)

        with pytest.raises(HTTPException) as e:
            await get_current_admin(mock_users[0], mock_user_service)
        assert e.value.status_code == 403
