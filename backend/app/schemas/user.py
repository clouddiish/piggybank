from typing import ClassVar

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserUpdate(UserBase):
    role_id: int
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserInDB(UserBase):
    password_hash: str


class UserOut(UserBase):
    role_id: int
    id: int


class UserFilters(BaseModel):
    role_id: list[int] | None = None
    email: list[str] | None = None

    list_filters: ClassVar[list[str]] = ["role_id", "email"]
    gt_filters: ClassVar[list[str]] = []
    lt_filters: ClassVar[list[str]] = []
    kw_filters: ClassVar[list[str]] = []

    model_config = {"extra": "forbid"}
