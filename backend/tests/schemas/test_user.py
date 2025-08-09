from pydantic import ValidationError
import pytest

from app.schemas import UserCreate, UserUpdate, UserOut, UserFilters


@pytest.mark.unit
class TestUserSchemas:
    @pytest.mark.anyio
    async def test_UserCreate__all_ok(self):
        data = {"role_id": 1, "email": "test@example.com", "password": "strongpass"}
        user = UserCreate(**data)

        assert user.role_id == 1
        assert user.email == "test@example.com"
        assert user.password == "strongpass"

    @pytest.mark.anyio
    async def test_UserCreate__extra_field(self):
        data = {
            "role_id": 1,
            "email": "test@example.com",
            "password": "strongpass",
            "extra": "not allowed",
        }
        with pytest.raises(ValidationError) as e:
            UserCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_UserCreate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            UserCreate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_UserCreate__invalid_type(self):
        data = {"role_id": "wrong", "email": 123, "password": "strongpass"}
        with pytest.raises(ValidationError) as e:
            UserCreate(**data)

        assert "Input should be a valid integer" in str(e.value)
        assert "Input should be a valid string" in str(e.value)

    @pytest.mark.anyio
    async def test_UserCreate__password_too_short(self):
        data = {"role_id": 1, "email": "test@example.com", "password": "short"}
        with pytest.raises(ValidationError) as e:
            UserCreate(**data)

        assert "String should have at least 8 characters" in str(e.value)

    @pytest.mark.anyio
    async def test_UserUpdate__all_ok(self):
        data = {"role_id": 2, "email": "new@example.com", "password": "newstrongpass"}
        user = UserUpdate(**data)

        assert user.role_id == 2
        assert user.email == "new@example.com"
        assert user.password == "newstrongpass"

    @pytest.mark.anyio
    async def test_UserUpdate__extra_field(self):
        data = {
            "role_id": 2,
            "email": "new@example.com",
            "password": "newstrongpass",
            "extra": "not allowed",
        }
        with pytest.raises(ValidationError) as e:
            UserUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_UserUpdate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            UserUpdate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_UserUpdate__invalid_type(self):
        data = {"role_id": "wrong", "email": 123, "password": "strongpass"}
        with pytest.raises(ValidationError) as e:
            UserUpdate(**data)

        assert "Input should be a valid integer" in str(e.value)
        assert "Input should be a valid string" in str(e.value)

    @pytest.mark.anyio
    async def test_UserUpdate__password_too_short(self):
        data = {"role_id": 1, "email": "test@example.com", "password": "short"}
        with pytest.raises(ValidationError) as e:
            UserUpdate(**data)

        assert "String should have at least 8 characters" in str(e.value)

    @pytest.mark.anyio
    async def test_UserOut__all_ok(self):
        data = {"id": 1, "role_id": 1, "email": "test@example.com"}
        user = UserOut(**data)

        assert user.id == 1
        assert user.role_id == 1
        assert user.email == "test@example.com"

    @pytest.mark.anyio
    async def test_UserOut__missing_field(self):
        data = {"role_id": 1, "email": "test@example.com"}
        with pytest.raises(ValidationError) as e:
            UserOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_UserOut__invalid_type(self):
        data = {"id": "wrong", "role_id": "wrong", "email": 123}
        with pytest.raises(ValidationError) as e:
            UserOut(**data)

        assert "Input should be a valid integer" in str(e.value)
        assert "Input should be a valid string" in str(e.value)

    @pytest.mark.anyio
    async def test_UserFilters__all_ok(self):
        data = {"role_id": [1, 2], "email": ["a@example.com", "b@example.com"]}
        filters = UserFilters(**data)

        assert filters.role_id == [1, 2]
        assert filters.email == ["a@example.com", "b@example.com"]

    @pytest.mark.anyio
    async def test_UserFilters__None_ok(self):
        data = {}
        filters = UserFilters(**data)

        assert filters.role_id is None
        assert filters.email is None

    @pytest.mark.anyio
    async def test_UserFilters__extra_field(self):
        data = {"role_id": [1], "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            UserFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_UserFilters__invalid_type_role_id(self):
        data = {"role_id": "should be list"}
        with pytest.raises(ValidationError) as e:
            UserFilters(**data)

        assert "Input should be a valid list" in str(e.value)

    @pytest.mark.anyio
    async def test_UserFilters__invalid_type_email(self):
        data = {"email": "should be list"}
        with pytest.raises(ValidationError) as e:
            UserFilters(**data)

        assert "Input should be a valid list" in str(e.value)
