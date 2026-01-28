from typing import ClassVar

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    model_config = {"extra": "forbid"}

    type_id: int


class CategoryUpdate(CategoryBase):
    model_config = {"extra": "forbid"}


class CategoryOut(CategoryBase):
    id: int
    type_id: int
    user_id: int


class CategoryFilters(BaseModel):
    user_id: list[int] | None = None
    type_id: list[int] | None = None
    name: list[str] | None = None

    list_filters: ClassVar[list[str]] = ["user_id", "type_id", "name"]
    gt_filters: ClassVar[list[str]] = []
    lt_filters: ClassVar[list[str]] = []
    kw_filters: ClassVar[list[str]] = []

    model_config = {"extra": "forbid"}
