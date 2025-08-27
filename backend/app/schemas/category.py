from pydantic import BaseModel


class CategoryBase(BaseModel):
    type_id: int
    name: str


class CategoryCreate(CategoryBase):
    model_config = {"extra": "forbid"}


class CategoryUpdate(CategoryBase):
    model_config = {"extra": "forbid"}


class CategoryOut(CategoryBase):
    id: int
    user_id: int


class CategoryFilters(BaseModel):
    user_id: list[int] | None = None
    type_id: list[int] | None = None
    name: list[str] | None = None

    model_config = {"extra": "forbid"}
