from abc import ABC
from datetime import date

from pydantic import BaseModel

from algoralabs.common.functions import date_to_timestamp


class Base(ABC, BaseModel):
    class Config:
        # use enum values when using .dict() on object
        use_enum_values = True
        json_encoders = {
            date: date_to_timestamp
        }
