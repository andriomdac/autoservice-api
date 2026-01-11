from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserResponseSchema(BaseModel):
    id: int
    username: str


class UserList(BaseModel):
    id: int
    username: str
