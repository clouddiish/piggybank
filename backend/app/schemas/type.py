from typing import ClassVar

from pydantic import BaseModel

from app.common.enums import TypeName


class TypeBase(BaseModel):
    name: TypeName


class TypeCreate(TypeBase):
    model_config = {"extra": "forbid"}


class TypeUpdate(TypeBase):
    model_config = {"extra": "forbid"}


class TypeOut(TypeBase):
    id: int


class TypeFilters(BaseModel):
    name: list[TypeName] | None = None

    list_filters: ClassVar[list[str]] = ["name"]
    gt_filters: ClassVar[list[str]] = []
    lt_filters: ClassVar[list[str]] = []
    kw_filters: ClassVar[list[str]] = []

    model_config = {"extra": "forbid"}
