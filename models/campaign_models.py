from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String

from models.village_models import LocationCustom

UUID_HEX = uuid4().hex


class CampaignImage(db.Base):
    __tablename__ = "campaign_images"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    location_id = Column(String(255), ForeignKey("location_custom.id"), nullable=False)
    title = Column(String(255), index=True)
    contributed_by = Column(String(255), ForeignKey(User.id))
    url = Column(String(255), index=True)

    location = relationship("LocationCustom", back_populates="campaign_image")


class CampaignSlogan(db.Base):
    __tablename__ = "campaign_slogans"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    location_id = Column(String(255), ForeignKey("location_custom.id"), nullable=False)
    text = Column(String(512), index=True)
    contributed_by = Column(String(255), ForeignKey(User.id))

    location = relationship("LocationCustom", back_populates="campaign_slogan")
