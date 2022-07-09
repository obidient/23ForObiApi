import pydantic as pd
from typing import Optional


class VillageBase(pd.BaseModel):
    name: str
    location: str


class Village(VillageBase):
    id: str
    contributed_by: Optional[str] = None

    class Config:
        orm_mode = True


class UserVillageBase(pd.BaseModel):
    village: str
    user: str


class UserVillage(UserVillageBase):
    id: str

    class Config:
        orm_mode = True


class StateDetails(pd.BaseModel):
    id: str
    state_code: str
    current_governor: str
    state_capital: str

    class Config:
        orm_mode = True