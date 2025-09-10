from datetime import date
from pydantic import ValidationError
import pytest

from app.schemas import TransactionCreate, TransactionUpdate, TransactionOut, TransactionFilters


@pytest.mark.unit
class TestTransactionSchemas:
    @pytest.mark.anyio
    async def test_TransactionCreate__all_ok(self):
        data = {"type_id": 1, "category_id": 2, "date": date.today(), "value": 100.5, "comment": "Groceries"}
        transaction = TransactionCreate(**data)

        assert transaction.type_id == 1
        assert transaction.category_id == 2
        assert transaction.date == data["date"]
        assert transaction.value == 100.5
        assert transaction.comment == "Groceries"

    @pytest.mark.anyio
    async def test_TransactionCreate__optional_fields_none(self):
        data = {"type_id": 1, "category_id": None, "date": date.today(), "value": 20.0, "comment": None}
        transaction = TransactionCreate(**data)

        assert transaction.category_id is None
        assert transaction.comment is None

    @pytest.mark.anyio
    async def test_TransactionCreate__missing_field(self):
        data = {"type_id": 1, "category_id": 2, "value": 100.5}
        with pytest.raises(ValidationError) as e:
            TransactionCreate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionCreate__extra_field(self):
        data = {"type_id": 1, "category_id": 2, "date": date.today(), "value": 100.5, "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TransactionCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionCreate__invalid_type(self):
        data = {"type_id": "wrong", "category_id": 2, "date": date.today(), "value": 100.5}
        with pytest.raises(ValidationError) as e:
            TransactionCreate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionUpdate__all_ok(self):
        data = {"type_id": 2, "category_id": None, "date": date.today(), "value": 50.0, "comment": "Transport"}
        transaction = TransactionUpdate(**data)

        assert transaction.type_id == 2
        assert transaction.category_id is None
        assert transaction.date == data["date"]
        assert transaction.value == 50.0
        assert transaction.comment == "Transport"

    @pytest.mark.anyio
    async def test_TransactionUpdate__optional_fields_none(self):
        data = {"type_id": 2, "category_id": None, "date": date.today(), "value": 50.0, "comment": None}
        transaction = TransactionUpdate(**data)

        assert transaction.category_id is None
        assert transaction.comment is None

    @pytest.mark.anyio
    async def test_TransactionUpdate__missing_field(self):
        data = {"type_id": 2, "value": 50.0}
        with pytest.raises(ValidationError) as e:
            TransactionUpdate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionUpdate__extra_field(self):
        data = {"type_id": 2, "category_id": 3, "date": date.today(), "value": 50.0, "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TransactionUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionUpdate__invalid_type(self):
        data = {"type_id": 2, "category_id": "wrong", "date": date.today(), "value": 50.0}
        with pytest.raises(ValidationError) as e:
            TransactionUpdate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionOut__all_ok(self):
        data = {
            "id": 1,
            "user_id": 10,
            "type_id": 3,
            "category_id": 4,
            "date": date.today(),
            "value": 200.0,
            "comment": "Rent",
        }
        transaction = TransactionOut(**data)

        assert transaction.id == 1
        assert transaction.user_id == 10
        assert transaction.type_id == 3
        assert transaction.category_id == 4
        assert transaction.date == data["date"]
        assert transaction.value == 200.0
        assert transaction.comment == "Rent"

    @pytest.mark.anyio
    async def test_TransactionOut__optional_fields_none(self):
        data = {
            "id": 1,
            "user_id": 10,
            "type_id": 3,
            "category_id": None,
            "date": date.today(),
            "value": 200.0,
            "comment": None,
        }
        transaction = TransactionOut(**data)

        assert transaction.category_id is None
        assert transaction.comment is None

    @pytest.mark.anyio
    async def test_TransactionOut__missing_field(self):
        data = {"id": 1, "user_id": 10, "type_id": 3, "category_id": 4, "value": 200.0}
        with pytest.raises(ValidationError) as e:
            TransactionOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionOut__invalid_type(self):
        data = {"id": "wrong", "user_id": 10, "type_id": 3, "category_id": 4, "date": date.today(), "value": 200.0}
        with pytest.raises(ValidationError) as e:
            TransactionOut(**data)

        assert "Input should be a valid integer" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionFilters__all_ok(self):
        data = {
            "user_id": [1, 2],
            "type_id": [3],
            "category_id": [4, 5],
            "date_gt": date(2024, 1, 1),
            "date_lt": date(2024, 12, 31),
            "value_gt": 100.0,
            "value_lt": 500.0,
            "comment": ["Rent", "Groceries"],
        }
        filters = TransactionFilters(**data)

        assert filters.user_id == [1, 2]
        assert filters.type_id == [3]
        assert filters.category_id == [4, 5]
        assert filters.date_gt == date(2024, 1, 1)
        assert filters.date_lt == date(2024, 12, 31)
        assert filters.value_gt == 100.0
        assert filters.value_lt == 500.0
        assert filters.comment == ["Rent", "Groceries"]

    @pytest.mark.anyio
    async def test_TransactionFilters__None_ok(self):
        data = {}
        filters = TransactionFilters(**data)

        assert filters.user_id is None
        assert filters.type_id is None
        assert filters.category_id is None
        assert filters.date_gt is None
        assert filters.date_lt is None
        assert filters.value_gt is None
        assert filters.value_lt is None
        assert filters.comment is None

    @pytest.mark.anyio
    async def test_TransactionFilters__optional_fields_partial(self):
        data = {"user_id": [1], "comment": None}
        filters = TransactionFilters(**data)

        assert filters.user_id == [1]
        assert filters.comment is None
        assert filters.type_id is None
        assert filters.category_id is None

    @pytest.mark.anyio
    async def test_TransactionFilters__extra_field(self):
        data = {"user_id": [1], "extra": "not allowed"}
        with pytest.raises(ValidationError) as e:
            TransactionFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_TransactionFilters__invalid_type(self):
        data = {"user_id": "should be list"}
        with pytest.raises(ValidationError) as e:
            TransactionFilters(**data)

        assert "Input should be a valid list" in str(e.value)
