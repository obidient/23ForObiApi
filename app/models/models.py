from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime
import bigfastapi.db.database as _database
from uuid import uuid4

class Test(_database.Base):
    __tablename__ = "posts"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    text = Column(String(255), index=True)
