from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.common.enums import EntityType, RoleName
from app.common.exceptions import EntityNotFoundException, UserEmailAlreadyExistsException, ActionForbiddenException
from app.db_models import User, Role
from app.schemas import UserFilters, UserCreate, UserUpdate
from app.services import UserService


@pytest.mark.unit
class TestUserServices:
    @pytest.mark.anyio
    async def test_get_by_id__id_exists(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_users[0]

        user = await mock_user_service.get_by_id(entity_id=mock_users[0].id)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_user_service.get_by_id(entity_id=3)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_email__email_found(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_users[0]

        user = await mock_user_service.get_by_email(email="test1@email.com")

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_get_by_email__email_not_found(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        user = await mock_user_service.get_by_email(email="test100@email.com")

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        assert user is None

    @pytest.mark.anyio
    async def test_is_admin__role_matches(self, mock_user_service: UserService, mock_users: list[User]):
        admin_role = Role(id=1, name=RoleName.admin)
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[0])
        mock_user_service.role_service.get_by_name = AsyncMock(return_value=admin_role)

        result = await mock_user_service.is_admin(user_id=1)

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.role_service.get_by_name.assert_called_once()
        assert result is True

    @pytest.mark.anyio
    async def test_is_admin__role_does_not_match(self, mock_user_service: UserService, mock_users: list[User]):
        admin_role = Role(id=1, name=RoleName.admin)
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[1])
        mock_user_service.role_service.get_by_name = AsyncMock(return_value=admin_role)

        result = await mock_user_service.is_admin(user_id=1)

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.role_service.get_by_name.assert_called_once()
        assert result is False

    @pytest.mark.anyio
    async def test_is_admin__user_not_found(self, mock_user_service: UserService, mock_users: list[User]):
        mock_user_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.user)
        )
        mock_user_service.role_service.get_by_name = AsyncMock()

        with pytest.raises(EntityNotFoundException):
            await mock_user_service.is_admin(user_id=100)

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.role_service.get_by_name.assert_not_called()

    @pytest.mark.anyio
    async def test_get_all_with_filters__no_filters(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_users

        roles = await mock_user_service.get_all_with_filters()

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert roles == mock_users

    @pytest.mark.anyio
    async def test_get_all_with_filters__with_filters(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_users[1]]

        roles = await mock_user_service.get_all_with_filters(filters=UserFilters(role_id=[2]))

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert roles == [mock_users[1]]

    @pytest.mark.anyio
    async def test_validate_create__all_ok(self, mock_user_service: UserService) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=None)
        user_create = UserCreate(email="test@test.pl", password="testpassword")

        await mock_user_service._validate_create(create_schema=user_create)

        mock_user_service.get_by_email.assert_called_once()

    @pytest.mark.anyio
    async def test_validate_create__email_exists(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[0])
        user_create = UserCreate(email=mock_users[0].email, password="testpassword")

        with pytest.raises(UserEmailAlreadyExistsException):
            await mock_user_service._validate_create(create_schema=user_create)

        mock_user_service.get_by_email.assert_called_once()

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__UserCreate(self, mock_user_service: UserService) -> None:
        user_create = UserCreate(email="test@test.pl", password="testpassword")

        valid_fields = mock_user_service._get_create_or_update_valid_fields(
            schema=user_create, password_hash="testhash"
        )

        assert valid_fields == {"email": "test@test.pl", "password_hash": "testhash"}

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__UserUpdate(self, mock_user_service: UserService) -> None:
        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="old_password", new_password="new_password"
        )

        valid_fields = mock_user_service._get_create_or_update_valid_fields(
            schema=user_update, password_hash="testhash"
        )

        assert valid_fields == {"role_id": 1, "email": "test@test.pl", "password_hash": "testhash"}

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_user_service: UserService) -> None:
        mock_user_service._validate_create = AsyncMock()
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 2, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_create = UserCreate(email="test@test.pl", password="testpassword")
        user = await mock_user_service.create(create_schema=user_create)

        mock_user_service._validate_create.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(user, User)
        assert hasattr(user, "id")
        assert user.role_id == 2
        assert user.email == user_create.email
        assert user.password_hash == "testhash"

    @pytest.mark.anyio
    async def test_create__email_exists(self, mock_session: AsyncMock, mock_user_service: UserService) -> None:
        mock_user_service._validate_create = AsyncMock(
            side_effect=UserEmailAlreadyExistsException(email="test@test.pl")
        )
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 2, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_create = UserCreate(email="test@test.pl", password="testpassword")
        with pytest.raises(UserEmailAlreadyExistsException):
            await mock_user_service.create(create_schema=user_create)

        mock_user_service._validate_create.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__all_ok_admin(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=True)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=1, name="test admin"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with patch("app.services.user.verify_password", return_value=True):
            user = await mock_user_service._validate_update(
                entity_id=1, update_schema=user_update, updated_by=mock_users[0]
            )

        mock_user_service.get_by_id.assert_called_once()
        assert (
            mock_user_service.is_admin.call_count == 2
        )  # first when checking if can update at all, second when checking if can update roles
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_called_once()
        assert user == mock_users[2]

    @pytest.mark.anyio
    async def test_validate_update__all_ok_same_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=False)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=2, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=2, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with patch("app.services.user.verify_password", return_value=True):
            user = await mock_user_service._validate_update(
                entity_id=1, update_schema=user_update, updated_by=mock_users[2]
            )

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()  # skipped at first because first condition of or is true already
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_called_once()
        assert user == mock_users[2]

    @pytest.mark.anyio
    async def test_validate_update__user_id_does_not_exist(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.user)
        )
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=1, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(EntityNotFoundException):
            await mock_user_service._validate_update(entity_id=100, update_schema=user_update, updated_by=mock_users[0])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_not_called()
        mock_user_service.get_by_email.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__different_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=False)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=2, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=2, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(ActionForbiddenException):
            await mock_user_service._validate_update(entity_id=1, update_schema=user_update, updated_by=mock_users[1])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_not_called()
        mock_user_service.get_by_email.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__role_id_does_not_exist(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[0])
        mock_user_service.is_admin = AsyncMock(return_value=True)
        mock_user_service.role_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.role)
        )
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=100, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(EntityNotFoundException):
            await mock_user_service._validate_update(entity_id=1, update_schema=user_update, updated_by=mock_users[0])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_not_called()  # skipped because first condition of or is true already
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__cannot_update_roles(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=False)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=2, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(ActionForbiddenException):
            await mock_user_service._validate_update(entity_id=1, update_schema=user_update, updated_by=mock_users[2])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__cannot_update_role_protected_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[1])
        mock_user_service.is_admin = AsyncMock(return_value=True)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=2, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(ActionForbiddenException):
            await mock_user_service._validate_update(entity_id=1, update_schema=user_update, updated_by=mock_users[0])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__email_exists_different_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[0])
        mock_user_service.is_admin = AsyncMock(return_value=True)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=2, name="test role"))
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[1])

        user_update = UserUpdate(
            role_id=2, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(UserEmailAlreadyExistsException):
            await mock_user_service._validate_update(entity_id=1, update_schema=user_update, updated_by=mock_users[0])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_called_once()

    @pytest.mark.anyio
    async def test_validate_update__email_exists_same_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[0])
        mock_user_service.is_admin = AsyncMock(return_value=False)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=1, name="test admin"))
        mock_user_service.get_by_email = AsyncMock(return_value=mock_users[0])

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with patch("app.services.user.verify_password", return_value=True):
            user = await mock_user_service._validate_update(
                entity_id=1, update_schema=user_update, updated_by=mock_users[0]
            )

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        mock_user_service.role_service.get_by_id.assert_called_once()
        mock_user_service.get_by_email.assert_called_once()
        assert user == mock_users[0]

    @pytest.mark.anyio
    async def test_validate_update__old_password_does_not_match(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[0])
        mock_user_service.is_admin = AsyncMock(return_value=False)
        mock_user_service.role_service.get_by_id = AsyncMock(return_value=Role(id=1, name="test admin"))
        mock_user_service.get_by_email = AsyncMock(return_value=None)

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with patch("app.services.user.verify_password", return_value=False):
            with pytest.raises(ActionForbiddenException):
                await mock_user_service._validate_update(
                    entity_id=1, update_schema=user_update, updated_by=mock_users[0]
                )

    @pytest.mark.anyio
    async def test_update__all_ok(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service._validate_update = AsyncMock(return_value=mock_users[0])
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 1, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        user = await mock_user_service.update(entity_id=mock_users[0].id, update_schema=user_update)

        mock_user_service._validate_update.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert user.id == mock_users[0].id
        assert user.role_id == user_update.role_id
        assert user.email == user_update.email
        assert user.password_hash == "testhash"

    @pytest.mark.anyio
    async def test_update__entity_id_does_not_exist(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service._validate_update = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.user)
        )
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 1, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(EntityNotFoundException):
            await mock_user_service.update(entity_id=mock_users[0].id, update_schema=user_update)

        mock_user_service._validate_update.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()

    @pytest.mark.anyio
    async def test_update__action_forbidden(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service._validate_update = AsyncMock(
            side_effect=ActionForbiddenException(detail="cannot update role of protected user")
        )
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 1, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(ActionForbiddenException):
            await mock_user_service.update(entity_id=mock_users[0].id, update_schema=user_update)

        mock_user_service._validate_update.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()

    @pytest.mark.anyio
    async def test_update__email_exists(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service._validate_update = AsyncMock(
            side_effect=UserEmailAlreadyExistsException(email="test@test.pl")
        )
        mock_user_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"role_id": 1, "email": "test@test.pl", "password_hash": "testhash"}
        )

        user_update = UserUpdate(
            role_id=1, email="test@test.pl", old_password="oldpassword", new_password="newpassword"
        )
        with pytest.raises(UserEmailAlreadyExistsException):
            await mock_user_service.update(entity_id=mock_users[0].id, update_schema=user_update)

        mock_user_service._validate_update.assert_called_once()
        mock_user_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()

    @pytest.mark.anyio
    async def test_vaidate_delete__all_ok_same_user(
        self, mock_user_service: UserService, mock_users: list[User]
    ) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=False)

        user = await mock_user_service._validate_delete(entity_id=1, deleted_by=mock_users[2])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_not_called()  # skipped because first condition of or is true already
        assert user == mock_users[2]

    @pytest.mark.anyio
    async def test_vaidate_delete__all_ok_admin(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=True)

        user = await mock_user_service._validate_delete(entity_id=1, deleted_by=mock_users[0])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()
        assert user == mock_users[2]

    @pytest.mark.anyio
    async def test_vaidate_delete__different_user(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[2])
        mock_user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_user_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

        mock_user_service.get_by_id.assert_called_once()
        mock_user_service.is_admin.assert_called_once()

    @pytest.mark.anyio
    async def test_vaidate_delete__protected_user(self, mock_user_service: UserService, mock_users: list[User]) -> None:
        mock_user_service.get_by_id = AsyncMock(return_value=mock_users[1])
        mock_user_service.role_service.get_by_name = AsyncMock(return_value=Role(id=1, name="test admin"))

        with pytest.raises(ActionForbiddenException):
            await mock_user_service._validate_delete(entity_id=2, deleted_by=mock_users[1])

        mock_user_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[Role]
    ) -> None:
        mock_user_service._validate_delete = AsyncMock(return_value=mock_users[0])

        role = await mock_user_service.delete(entity_id=mock_users[0].id)

        mock_user_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert role == mock_users[0]

    @pytest.mark.anyio
    async def test_delete__protected_user(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[Role]
    ) -> None:
        mock_user_service._validate_delete = AsyncMock(
            side_effect=ActionForbiddenException(detail="cannot delete protected user")
        )

        with pytest.raises(ActionForbiddenException):
            await mock_user_service.delete(entity_id=mock_users[1].id)

        mock_user_service._validate_delete.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.anyio
    async def test_delete__id_does_not_exist(
        self, mock_session: AsyncMock, mock_user_service: UserService, mock_users: list[Role]
    ) -> None:
        mock_user_service._validate_delete = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.user)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_user_service.delete(entity_id=100)

        mock_user_service._validate_delete.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
