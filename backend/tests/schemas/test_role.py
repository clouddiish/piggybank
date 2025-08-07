from pydantic import ValidationError
import pytest

from app.schemas import RoleCreate, RoleUpdate, RoleOut, RoleFilters


@pytest.mark.unit
class TestRoleSchemas:
    @pytest.mark.anyio
    async def test_RoleCreate__all_ok(self):
        data = {"name": "test role"}
        role = RoleCreate(**data)

        assert role.name == "test role"

    @pytest.mark.anyio
    async def test_RoleCreate__extra_field(self):
        data = {"name": "test role", "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            RoleCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleCreate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            RoleCreate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleCreate__invalid_type(self):
        data = {"name": 123}
        with pytest.raises(ValidationError) as e:
            RoleCreate(**data)

        assert "Input should be a valid string" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleUpdate__all_ok(self):
        data = {"name": "test role"}
        role = RoleUpdate(**data)

        assert role.name == "test role"

    @pytest.mark.anyio
    async def test_RoleUpdate__extra_field(self):
        data = {"name": "test role", "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            RoleUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleUpdate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            RoleUpdate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleUpdate__invalid_type(self):
        data = {"name": 123}
        with pytest.raises(ValidationError) as e:
            RoleUpdate(**data)

        assert "Input should be a valid string" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleOut__all_ok(self):
        data = {"id": 1, "name": "test role"}
        role = RoleOut(**data)

        assert role.id == 1
        assert role.name == "test role"

    @pytest.mark.anyio
    async def test_RoleOut__missing_field(self):
        data = {"name": "test role"}
        with pytest.raises(ValidationError) as e:
            RoleOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleOut__invalid_type(self):
        data = {"id": "wrong", "name": "test role"}
        with pytest.raises(ValidationError) as e:
            RoleOut(**data)

        assert "Input should be a valid integer" in str(e.value)

    @pytest.mark.anyio
    async def test_RoleFilters__all_ok(self):
        data = {"name": ["test role"]}
        filters = RoleFilters(**data)

        assert filters.name == ["test role"]

    @pytest.mark.anyio
    async def test_RoleFilters__None_ok(self):
        data = {}
        filters = RoleFilters(**data)

        assert filters.name is None

    @pytest.mark.anyio
    async def test_RoleFilters__extra_field(self):
        data = {"name": "test role", "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            RoleFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def testRoleFilters__invalid_type(self):
        data = {"name": "should be list"}
        with pytest.raises(ValidationError) as e:
            RoleFilters(**data)

        assert "Input should be a valid list" in str(e.value)
