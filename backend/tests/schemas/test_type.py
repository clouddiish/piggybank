from pydantic import ValidationError
import pytest

from app.common.enums import TypeName
from app.schemas import TypeCreate, TypeUpdate, TypeOut, TypeFilters


@pytest.mark.unit
class TestTypeSchemas:
    @pytest.mark.anyio
    async def test_TypeCreate__all_ok(self):
        data = {"name": TypeName.expense}
        type = TypeCreate(**data)

        assert type.name == TypeName.expense

    @pytest.mark.anyio
    async def test_TypeCreate__extra_field(self):
        data = {"name": TypeName.expense, "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TypeCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeCreate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            TypeCreate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeCreate__invalid_type(self):
        data = {"name": 123}
        with pytest.raises(ValidationError) as e:
            TypeCreate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeUpdate__all_ok(self):
        data = {"name": TypeName.expense}
        type = TypeUpdate(**data)

        assert type.name == TypeName.expense

    @pytest.mark.anyio
    async def test_TypeUpdate__extra_field(self):
        data = {"name": TypeName.expense, "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TypeUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeUpdate__missing_field(self):
        with pytest.raises(ValidationError) as e:
            TypeUpdate()

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeUpdate__invalid_type(self):
        data = {"name": 123}
        with pytest.raises(ValidationError) as e:
            TypeUpdate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeOut__all_ok(self):
        data = {"id": 1, "name": TypeName.expense}
        type = TypeOut(**data)

        assert type.id == 1
        assert type.name == TypeName.expense

    @pytest.mark.anyio
    async def test_TypeOut__missing_field(self):
        data = {"name": TypeName.expense}
        with pytest.raises(ValidationError) as e:
            TypeOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeOut__invalid_type(self):
        data = {"id": "wrong", "name": TypeName.expense}
        with pytest.raises(ValidationError) as e:
            TypeOut(**data)

        assert "Input should be a valid integer" in str(e.value)

    @pytest.mark.anyio
    async def test_TypeFilters__all_ok(self):
        data = {"name": [TypeName.expense]}
        filters = TypeFilters(**data)

        assert filters.name == [TypeName.expense]

    @pytest.mark.anyio
    async def test_TypeFilters__None_ok(self):
        data = {}
        filters = TypeFilters(**data)

        assert filters.name is None

    @pytest.mark.anyio
    async def test_TypeFilters__extra_field(self):
        data = {"name": [TypeName.expense], "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TypeFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def testTypeFilters__invalid_type(self):
        data = {"name": "should be list"}
        with pytest.raises(ValidationError) as e:
            TypeFilters(**data)

        assert "Input should be a valid list" in str(e.value)
