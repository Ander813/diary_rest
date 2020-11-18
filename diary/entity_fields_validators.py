import re
from rest_framework.serializers import ValidationError


class AbstractEntityValidator:

    types = [r"^string$", r"^number$", "^boolean$"]

    def is_allowed(self, field_name):
        for type_ in self.types:
            if re.match(type_, field_name):
                return True
        return False

    def validate(self, entity):
        if type(entity) is not dict:
            try:
                entity = dict(entity)
            except TypeError:
                raise ValidationError('Entity must be dict or could be converted to dict')
        for entity_field_type in entity.values():
            if not self.is_allowed(entity_field_type):
                raise ValidationError(f"{entity_field_type} is not allowed for model")
        return entity


class EntityValidator:

    types = {
        "string": str,
        "number": float,
        "boolean": bool,
    }

    def validate(self, parent_entity, child_entity):
        assert type(parent_entity) is dict and type(child_entity) is dict, \
            (f"parent_entity and child_entity must be dicts")

        for key, value in parent_entity.items():
            if key in child_entity:
                if type(child_entity[key]) is not self.types[value]:
                    raise ValidationError(f'Field {key} must be {value}, '
                                          f'got {type(child_entity[key])}')
            else:
                raise ValidationError(f'Expected {key} in entity')

        return child_entity
