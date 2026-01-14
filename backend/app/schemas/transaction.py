from datetime import date
from typing import ClassVar

from pydantic import BaseModel


class TransactionBase(BaseModel):
    type_id: int
    category_id: int | None = None
    date: date
    value: float
    comment: str | None = None


class TransactionCreate(TransactionBase):
    model_config = {"extra": "forbid"}


class TransactionUpdate(TransactionBase):
    model_config = {"extra": "forbid"}


class TransactionOut(TransactionBase):
    id: int
    user_id: int


class TransactionTotalOut(BaseModel):
    total: float


class TransactionFilters(BaseModel):
    user_id: list[int] | None = None
    type_id: list[int] | None = None
    category_id: list[int] | None = None
    date_gt: date | None = None
    date_lt: date | None = None
    value_gt: float | None = None
    value_lt: float | None = None
    comment: list[str] | None = None

    list_filters: ClassVar[list[str]] = ["user_id", "type_id", "category_id"]
    gt_filters: ClassVar[list[str]] = ["date_gt", "value_gt"]
    lt_filters: ClassVar[list[str]] = ["date_lt", "value_lt"]
    kw_filters: ClassVar[list[str]] = ["comment"]

    model_config = {"extra": "forbid"}
