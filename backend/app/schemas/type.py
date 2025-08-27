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

    model_config = {"extra": "forbid"}
