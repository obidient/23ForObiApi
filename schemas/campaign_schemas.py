from typing import Optional

import pydantic as pd


class CampaignImageBase(pd.BaseModel):
    location: str
    title: str
    url: str
    contributed_by: Optional[str] = None


class CampaignImage(CampaignImageBase):
    id: str

    class Config:
        orm_mode = True
