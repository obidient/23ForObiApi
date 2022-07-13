import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.contact_model import ContactUs
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, String

from models.village_models import Village

UUID_HEX = uuid4().hex


class Voter(db.Base):
    __tablename__ = "voters"
    id = Column(String(50), primary_key=True, index=True, default=UUID_HEX)
    village_id = Column(String(255), ForeignKey("villages.id"))
    name = Column(String(255), index=True)
    contact = Column(String(255), ForeignKey(ContactUs.id))
    notes = Column(String(255), index=True)
    importance = Column(String(255), index=True)
    date_delivered = Column(DateTime, default=datetime.datetime.utcnow)
    delivered_by = Column(String(255), ForeignKey(User.id))

    village = relationship(Village, back_populates="voters")


class DuplicatedVoter(db.Base):
    __tablename__ = "duplicated_voters"
    id = Column(String(50), primary_key=True, index=True, default=UUID_HEX)
