from app.common.enums import EntityType


class EntityNotFoundException(Exception):
    def __init__(self, entity_id: int, entity_type: EntityType):
        self.entity_id = entity_id
        self.entity_type = entity_type
        super().__init__(f"{entity_type.value} with id {entity_id} not found")


class RoleNotFoundException(Exception):
    pass
