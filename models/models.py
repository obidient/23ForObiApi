import datetime as datetime
from uuid import uuid4

import bigfastapi.db.database as db
from bigfastapi.models.user_models import User
from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.schema import Column
from models.village_models import LocationCustom, Village

UUID_HEX = uuid4().hex


class Test(db.Base):
    __tablename__ = "test"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    text = Column(String(255), index=True)
