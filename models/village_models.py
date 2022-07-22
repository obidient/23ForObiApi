import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String


class StateDetails(db.Base):
    __tablename__ = "state_details"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    state_code = Column(String(2), nullable=False)
    current_governor = Column(String(50), nullable=True)
    state_capital = Column(String(50), nullable=True)


class LocationCustom(db.Base):
    __tablename__ = "location_custom"

    id = Column(String(255), primary_key=True, index=True, default="QQ")
    country = Column(String(255), nullable=False)
    current_governor = Column(String(50), nullable=True)
    state_name = Column(String(50), nullable=True)
    state_capital = Column(String(50), nullable=True)
    current_governor_appointment_date = Column(String(50), nullable=True)
    last_vote_direction = Column(String(50), nullable=True)
    progress = Column(Integer(), nullable=True)
    vote_control = Column(Integer(), nullable=True)

    village = relationship("Village", back_populates="location")


class Village(db.Base):
    __tablename__ = "villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    name = Column(String(255), index=True)
    location_id = Column(String(255), ForeignKey("location_custom.id"))
    contributed_by = Column(String(255), ForeignKey(User.id), nullable=True)

    voters = relationship("Voter", back_populates="village")
    location = relationship("LocationCustom", back_populates="village")


class UserVillage(db.Base):
    __tablename__ = "user_villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    village = Column(String(255), ForeignKey(Village.id))
    user = Column(String(255), ForeignKey(User.id))
