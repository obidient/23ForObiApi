from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter
from models import campaign_models
from schemas import campaign_schemas

app = APIRouter()


@app.post("/campaign_images/")
async def create_campaign_image(
    campaign_image: campaign_schemas.CampaignImageBase,
    db: Session = fastapi.Depends(get_db),
):
    db_campaign_image = campaign_models.CampaignImage(
        id=uuid4().hex,
        location=campaign_image.location,
        title=campaign_image.title,
        url=campaign_image.url,
        contributed_by=campaign_image.contributed_by,
    )
    db.add(db_campaign_image)
    db.commit()
    db.refresh(db_campaign_image)
    return {
        "message": "Campaign Image added succesfully",
        "support_group": campaign_schemas.CampaignImage.from_orm(db_campaign_image),
    }


@app.get(
    "/campaign-images/{state_id}", response_model=List[campaign_schemas.CampaignImage]
)
async def list_campaign_images(state_id: str, db: Session = fastapi.Depends(get_db)):
    campaign_images = db.query(campaign_models.CampaignImage).filter(
        campaign_models.CampaignImage.location == state_id
    )
    return list(map(campaign_schemas.CampaignImage.from_orm, campaign_images))
