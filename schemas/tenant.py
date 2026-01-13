from datetime import datetime
from pydantic import BaseModel
from schemas.users import UserResponseSchema


class TenantRequestSchema(BaseModel):
    name: str


class TenantResponseSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    users: list[UserResponseSchema]
