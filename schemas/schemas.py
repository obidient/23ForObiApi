from typing import Optional

from bigfastapi.schemas.users_schemas import User as UserSchema
from pydantic import BaseModel


class TestSchema(BaseModel):
    text: str

    class Config:
        orm_mode = True


class GoogleToken(BaseModel):
    token: str

    class Config:
        orm_mode = True


class UserSchemaCustom(UserSchema):
    image_url: Optional[str] = None
    google_image_url: Optional[str] = None

    class Config:
        orm_mode = True


class CreateUserDataSchema(BaseModel):
    data: dict
    is_village_new : bool = False
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
