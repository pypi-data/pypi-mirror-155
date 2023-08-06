from enum import Enum
from algoralabs.common.base import Base


class PermissionType(Enum):
    USER_ID = "USER_ID"
    GROUP = "GROUP"
    ROLE = "ROLE"


class PermissionRequest(Base):
    resource_id: str
    permission_type: PermissionType
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool