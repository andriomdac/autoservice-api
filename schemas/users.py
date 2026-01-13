from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str
    tenant_id: int
    role_id: int


class UserAdminCreateSchema(BaseModel):
    username: str
    password: str
    tenant_name: str


class UserResponseSchema(BaseModel):
    id: int
    username: str
    tenant_id: int
    role_id: int


class UserUpdateSchema(BaseModel):
    password: str
    new_password: str
