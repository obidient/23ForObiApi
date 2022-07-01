import pydantic as pd


class VillageBase(pd.BaseModel):
    name: str
    location: str
    contributed_by: str


class Village(VillageBase):
    id: str

    class Config:
        orm_mode = True


class VillageCreate(VillageBase):
    pass


class VillageUpdate(VillageBase):
    pass


class UserVillageBase(pd.BaseModel):
    village: str
    user: str


class UserVillage(UserVillageBase):
    id: str

    class Config:
        orm_mode = True


class UserVillageCreate(UserVillageBase):
    pass


class UserVillageUpdate(UserVillageBase):
    pass
