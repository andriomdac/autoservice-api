from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserResponseSchema(BaseModel):
    username: str
    uuid: str


class UserList(BaseModel):
    uuid: str
    username: str
