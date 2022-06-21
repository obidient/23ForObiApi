from sqlalchemy.schema import Column
from sqlalchemy.types import String
import bigfastapi.db.database as db
from uuid import uuid4

class Test(db.Base):
    __tablename__ = "test"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    text = Column(String(255), index=True)
