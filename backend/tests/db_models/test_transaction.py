from datetime import date

import pytest

from app.db_models import Transaction


@pytest.mark.unit
class TestTransactionDbModel:
    @pytest.mark.anyio
    async def test_transaction_model__all_ok(self):
        transaction = Transaction(
            user_id=1,
            type_id=1,
            category_id=1,
            date=date(year=2025, month=9, day=1),
            value=10.5,
            comment="Test comment",
        )

        assert hasattr(transaction, "id")
        assert transaction.user_id == 1
        assert transaction.type_id == 1
        assert transaction.category_id == 1
        assert transaction.date == date(year=2025, month=9, day=1)
        assert transaction.value == 10.5
        assert transaction.comment == "Test comment"
