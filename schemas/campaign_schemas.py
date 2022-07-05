from typing import Optional

import pydantic as pd


class CampaignImageBase(pd.BaseModel):
    location: str
    title: str
    url : str


class CampaignImage(CampaignImageBase):
    id: str
    contributed_by: str

    class Config:
        orm_mode = True
