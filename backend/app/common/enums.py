from enum import Enum


class Tag(Enum):
    category = "category"
    goal = "goal"
    role = "role"
    transaction = "transaction"
    type = "type"
    user = "user"
    security = "security"


class EntityType(Enum):
    role = "role"
    user = "user"
    type = "type"
    goal = "goal"
    category = "category"
    transaction = "transaction"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
