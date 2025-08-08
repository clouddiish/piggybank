from app.common.enums import EntityType


class EntityNotFoundException(Exception):
    def __init__(self, entity_id: int, entity_type: EntityType):
        self.entity_id = entity_id
        self.entity_type = entity_type
        super().__init__(f"{entity_type.value} with id {entity_id} not found")


class UserEmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"user with email {email} already exists")


class ActionForbiddenException(Exception):
    def __init__(self, detail: str = ""):
        self.detail = detail
        super().__init__(f"action forbidden{f': {detail}' if detail else ''}")
