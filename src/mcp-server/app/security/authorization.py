from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    SRE = "sre"
    VIEWER = "viewer"

def authorize_user(user: dict, action: str) -> bool:
    # Authorize user using RBAC
    pass