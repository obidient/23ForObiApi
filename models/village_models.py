import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.user_models import User
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
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
    slug = Column(String(255), nullable=True)

    village = relationship("Village", back_populates="location")
    user_villages = relationship("UserVillage", back_populates="location")
    user_data = relationship("UserData", back_populates="location")
    local_government = relationship("LocalGovernment", back_populates="location")


class LocalGovernment(db.Base):
    __tablename__ = "local_governments"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    name = Column(String(255), nullable=False)
    location_id = Column(String(255), ForeignKey("location_custom.id"), nullable=False)

    location = relationship("LocationCustom", back_populates="local_government")
    village = relationship("Village", back_populates="local_government")
    user_data = relationship("UserData", back_populates="local_government")


class Village(db.Base):
    __tablename__ = "villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    name = Column(String(255), index=True)
    location_id = Column(String(255), ForeignKey("location_custom.id"))
    local_government_id = Column(
        String(255), ForeignKey("local_governments.id"), nullable=True
    )
    contributed_by = Column(String(255), ForeignKey(User.id), nullable=True)
    is_active = Column(Boolean, default=True)

    voters = relationship("Voter", back_populates="village")
    location = relationship("LocationCustom", back_populates="village")
    user_villages = relationship("UserVillage", back_populates="village")
    user_data = relationship("UserData", back_populates="village_id")
    local_government = relationship("LocalGovernment", back_populates="village")


class UserVillage(db.Base):
    __tablename__ = "user_villages"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    village_id = Column(String(255), ForeignKey("villages.id"))
    state_id = Column(String(255), ForeignKey("location_custom.id"))
    user = Column(String(255), ForeignKey(User.id))

    village = relationship(Village, back_populates="user_villages")
    location = relationship(LocationCustom, back_populates="user_villages")


class UserData(db.Base):
    __tablename__ = "user_data"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    user = Column(String(255), ForeignKey(User.id), nullable=True)
    data = Column(JSON, default={})
    state = Column(String(255), ForeignKey("location_custom.id"), nullable=True)
    local_government_id = Column(
        String(255), ForeignKey("local_governments.id"), nullable=True
    )
    village = Column(String(255), ForeignKey("villages.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    local_government = relationship(LocalGovernment, back_populates="user_data")
    village_id = relationship(Village, back_populates="user_data")
    location = relationship(LocationCustom, back_populates="user_data")
