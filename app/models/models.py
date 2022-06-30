import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.contact_model import ContactUs
from bigfastapi.models.location_models import Location
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, String


class Test(db.Base):
    __tablename__ = "test"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    text = Column(String(255), index=True)


class Village(db.Base):
    __tablename__ = "villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    name = Column(String(255), index=True)
    location = Column(String(255), ForeignKey("locations.id"))
    contributed_by = Column(String(255), ForeignKey("users.id"))


class Voter(db.Base):
    __tablename__ = "voters"
    id = Column(String(50), primary_key=True, index=True, default=uuid4().hex)
    village = Column(String(255), ForeignKey("villages.id"))
    name = Column(String(255), index=True)
    contact = Column(String(255), ForeignKey("contactus.id"))
    notes = Column(String(255), index=True)
    importance = Column(String(255), index=True)
    date_delivered = Column(DateTime, default=datetime.datetime.utcnow)
    delivered_by = Column(String(255), ForeignKey("users.id"))


class DuplicatedVoter(db.Base):
    __tablename__ = "duplicated_voters"
    id = Column(String(50), primary_key=True, index=True, default=uuid4().hex)


class UserVillage(db.Base):
    __tablename__ = "user_villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    village = Column(String(255), ForeignKey("villages.id"))
    user = Column(String(255), ForeignKey("users.id"))


class CampaignImage(db.Base):
    __tablename__ = "campaign_images"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    location = Column(String(255), ForeignKey("locations.id"))
    title = Column(String(255), index=True)
    contributed_by = Column(String(255), ForeignKey("users.id"))
    url = Column(String(255), index=True)


class CampaignSlogan(db.Base):
    __tablename__ = "campaign_slogans"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    location = Column(String(255), ForeignKey("locations.id"))
    text = Column(String(512), index=True)
    contributed_by = Column(String(255), ForeignKey("users.id"))


class SupportGroup(db.Base):
    __tablename__ = "support_groups"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    name = Column(String(255), index=True)
    votes_delivered = Column(Integer, default=0)
