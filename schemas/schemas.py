from typing import Optional
from pydantic import BaseModel


class TestSchema(BaseModel):
    text: str

    class Config:
        orm_mode = True


class GoogleToken(BaseModel):
    token: str

    class Config:
        orm_mode = True


class CreateUserDataSchema(BaseModel):
    data: dict
    # state: Optional[str] = None
    # village: Optional[str] = None


class UserDataSchema(CreateUserDataSchema):
    id: str
    user: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    state: str
    village: str

    class Config:
        orm_mode = True
