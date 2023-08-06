from enum import Enum
from algoralabs.common.base import Base


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


class Field(Base):
    logical_name: str
    type: FieldType
