from typing import Optional

import pydantic as pd


class SupportGroupBase(pd.BaseModel):
    name: str
    votes_delivered: Optional[int] = 0


class SupportGroup(SupportGroupBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True
