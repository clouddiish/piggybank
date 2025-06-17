from enum import Enum


class Tag(Enum):
    category = "category"
    goal = "goal"
    role = "role"
    transaction = "transaction"
    type = "type"
    user = "user"


class EntityType(Enum):
    role = "role"
    user = "user"
    type = "type"
    goal = "goal"
    category = "category"
    transaction = "transaction"
