from pydantic import BaseModel, Field


class UserBase(BaseModel):
    role_id: int
    email: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserUpdate(UserBase):
    password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserInDB(UserBase):
    password_hash: str


class UserOut(UserBase):
    id: int


class UserFilters(BaseModel):
    model_config = {"extra": "forbid"}

    role_id: list[int] | None = None
    email: list[str] | None = None
