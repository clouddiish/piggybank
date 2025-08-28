from pydantic import ValidationError
import pytest

from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut, CategoryFilters


@pytest.mark.unit
class TestCategorySchemas:
    @pytest.mark.anyio
    async def test_CategoryCreate__all_ok(self):
        data = {"type_id": 1, "name": "Food"}
        category = CategoryCreate(**data)

        assert category.type_id == 1
        assert category.name == "Food"

    @pytest.mark.anyio
    async def test_CategoryCreate__extra_field(self):
        data = {"type_id": 1, "name": "Food", "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            CategoryCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryCreate__missing_field(self):
        data = {"type_id": 1}
        with pytest.raises(ValidationError) as e:
            CategoryCreate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryCreate__invalid_type(self):
        data = {"type_id": "wrong", "name": "Food"}
        with pytest.raises(ValidationError) as e:
            CategoryCreate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryUpdate__all_ok(self):
        data = {"type_id": 2, "name": "Transport"}
        category = CategoryUpdate(**data)

        assert category.type_id == 2
        assert category.name == "Transport"

    @pytest.mark.anyio
    async def test_CategoryUpdate__extra_field(self):
        data = {"type_id": 2, "name": "Transport", "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            CategoryUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryUpdate__missing_field(self):
        data = {"name": "Transport"}
        with pytest.raises(ValidationError) as e:
            CategoryUpdate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryUpdate__invalid_type(self):
        data = {"type_id": "wrong", "name": "Transport"}
        with pytest.raises(ValidationError) as e:
            CategoryUpdate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryOut__all_ok(self):
        data = {"id": 1, "user_id": 2, "type_id": 3, "name": "Shopping"}
        category = CategoryOut(**data)

        assert category.id == 1
        assert category.user_id == 2
        assert category.type_id == 3
        assert category.name == "Shopping"

    @pytest.mark.anyio
    async def test_CategoryOut__missing_field(self):
        data = {"id": 1, "user_id": 2, "type_id": 3}
        with pytest.raises(ValidationError) as e:
            CategoryOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryOut__invalid_type(self):
        data = {"id": "wrong", "user_id": 2, "type_id": 3, "name": "Shopping"}
        with pytest.raises(ValidationError) as e:
            CategoryOut(**data)

        assert "Input should be a valid integer" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryFilters__all_ok(self):
        data = {"user_id": [1, 2], "type_id": [3], "name": ["Food", "Travel"]}
        filters = CategoryFilters(**data)

        assert filters.user_id == [1, 2]
        assert filters.type_id == [3]
        assert filters.name == ["Food", "Travel"]

    @pytest.mark.anyio
    async def test_CategoryFilters__None_ok(self):
        data = {}
        filters = CategoryFilters(**data)

        assert filters.user_id is None
        assert filters.type_id is None
        assert filters.name is None

    @pytest.mark.anyio
    async def test_CategoryFilters__extra_field(self):
        data = {"user_id": [1], "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            CategoryFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_CategoryFilters__invalid_type(self):
        data = {"user_id": "should be list"}
        with pytest.raises(ValidationError) as e:
            CategoryFilters(**data)

        assert "Input should be a valid list" in str(e.value)
