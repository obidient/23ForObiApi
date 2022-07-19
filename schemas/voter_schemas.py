import datetime as dt
from typing import Optional

import pydantic as pd


class VoterSchemaBase(pd.BaseModel):
    name: str
    village_id: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    importance: Optional[str] = None


class VoterSchema(VoterSchemaBase):
    id: str
    date_delivered: dt.datetime
    delivered_by: Optional[str] = None

    class Config:
        orm_mode = True
