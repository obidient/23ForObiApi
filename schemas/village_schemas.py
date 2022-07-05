import pydantic as pd


class VillageBase(pd.BaseModel):
    name: str
    location: str
    contributed_by: str


class Village(VillageBase):
    id: str

    class Config:
        orm_mode = True


class UserVillageBase(pd.BaseModel):
    village: str
    user: str


class UserVillage(UserVillageBase):
    id: str

    class Config:
        orm_mode = True
