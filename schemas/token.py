from pydantic import BaseModel


class GenerateTokenRequestSchema(BaseModel):
    username: str
    password: str


class GenerateTokenResponseSchema(BaseModel):
    access: str
    claims: dict


class VerifyTokenRequestSchema(BaseModel):
    token: str
