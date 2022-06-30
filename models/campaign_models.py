from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.location_models import Location
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import String

UUID_HEX = uuid4().hex


class CampaignImage(db.Base):
    __tablename__ = "campaign_images"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    location = Column(String(255), ForeignKey(Location.id))
    title = Column(String(255), index=True)
    contributed_by = Column(String(255), ForeignKey(User.id))
    url = Column(String(255), index=True)


class CampaignSlogan(db.Base):
    __tablename__ = "campaign_slogans"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    location = Column(String(255), ForeignKey(Location.id))
    text = Column(String(512), index=True)
    contributed_by = Column(String(255), ForeignKey(User.id))
