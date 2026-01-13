from pydantic import BaseModel


class RoleResponseSchema(BaseModel):
    id: int
    name: str


class RoleRequestSchema(BaseModel):
    name: str
