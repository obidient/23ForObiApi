from uuid import uuid4

import bigfastapi.db.database as db
from sqlalchemy.schema import Column
from sqlalchemy.types import String

UUID_HEX = uuid4().hex


class Test(db.Base):
    __tablename__ = "test"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    text = Column(String(255), index=True)
