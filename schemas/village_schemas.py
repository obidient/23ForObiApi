from typing import Optional

import pydantic as pd


class VillageBase(pd.BaseModel):
    name: str
    location_id: str


class Village(VillageBase):
    id: str
    contributed_by: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


class UserVillageBase(pd.BaseModel):
    village_id: str


class UserVillage(UserVillageBase):
    id: str
    village_id: Village

    class Config:
        orm_mode = True


class StateDetails(pd.BaseModel):
    id: str
    country: str
    current_governor: Optional[str] = None
    state_capital: Optional[str] = None
    state_name: Optional[str] = None
    current_governor_appointment_date: Optional[str] = None
    last_vote_direction: Optional[str] = None
    progress: Optional[int] = 0
    vote_control: Optional[int] = 0
    slug: Optional[str] = None

    class Config:
        orm_mode = True
