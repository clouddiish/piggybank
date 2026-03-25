import re
from datetime import date
from typing import ClassVar

from pydantic import BaseModel, field_validator

from app.core.config import get_settings


settings = get_settings()


class TransactionBase(BaseModel):
    type_id: int
    category_id: int | None = None
    date: date
    value: float
    comment: str | None = None

    @field_validator("comment", mode="before")
    def validate_comment(cls, v: str | None) -> str | None:
        if v is None:
            return v

        # ensure the comment is at most 255 characters
        if len(v) > 255:
            raise ValueError("comment should have at most 255 characters")

        # disallow dangerous characters
        if re.search(settings.comment_disallowed_chars, v):
            raise ValueError("comment contains invalid characters")

        # disallow control characters
        if any(ord(c) < 32 for c in v):  # ASCII control characters
            raise ValueError("comment contains control characters")

        return v


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
