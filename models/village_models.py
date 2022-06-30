import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.location_models import Location
from bigfastapi.models.user_models import User
from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import String

UUID_HEX = uuid4().hex


class Village(db.Base):
    __tablename__ = "villages"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    name = Column(String(255), index=True)
    location = Column(String(255), ForeignKey(Location.id))
    contributed_by = Column(String(255), ForeignKey(User.id))


class UserVillage(db.Base):
    __tablename__ = "user_villages"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    village = Column(String(255), ForeignKey(Village.id))
    user = Column(String(255), ForeignKey(User.id))
