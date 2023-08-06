from abc import ABC
from datetime import date
from enum import Enum

from pydantic import BaseModel

from algoralabs.common.functions import date_to_timestamp


class BaseEnum(str, Enum):
    """Inheriting from str is necessary to correctly serialize output of enum"""
    pass


class Base(ABC, BaseModel):
    class Config:
        # use enum values when using .dict() on object
        use_enum_values = True
        json_encoders = {
            date: date_to_timestamp
        }
