from enum import Enum
from typing import Optional, List
from algoralabs.common.base import Base

from algoralabs.common.enum import FieldType


class DatasetDataType(Enum):
    STOCK = 'STOCK'


class DatasetRequest(Base):
    display_name: str
    logical_name: str
    description: Optional[str]
    data_type: DatasetDataType
    data_query: str
    data_query_type: str
    schema_id: str
    directory_id: str


class DatasetSearchRequest(Base):
    query: str
    data_types: Optional[List[str]]  # TODO make enum


class DatasetSummaryResponse(Base):
    id: str
    display_name: str
    logical_name: str
    description: Optional[str]
    data_type: str  # TODO make enum
    tag: str


class FieldRequest(Base):
    display_name: str
    logical_name: str
    type: FieldType
    width: int
    editable: bool
    hidden: bool
    display_order: int
    tags: List[str]  # TODO make enum
    schema_id: str
    field_group_id: Optional[str]


class FieldGroupRequest(Base):
    display_name: str
    logical_name: str


class SchemaRequest(Base):
    display_name: str
    logical_name: str


class SchemaResponse(Base):
    id: str
    display_name: str
    logical_name: str
