import datetime
from uuid import uuid4

import bigfastapi.db.database as db
from sqlalchemy import Integer, Boolean
from sqlalchemy.schema import Column
from sqlalchemy.types import String

UUID_HEX = uuid4().hex


class SupportGroup(db.Base):
    __tablename__ = "support_groups"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    name = Column(String(255), index=True)
    votes_delivered = Column(Integer, default=0)
    is_active = Column(Boolean, default=False)
