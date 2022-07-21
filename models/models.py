import datetime as datetime
from uuid import uuid4

import bigfastapi.db.database as db
from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, DateTime, String, Text

UUID_HEX = uuid4().hex


class Test(db.Base):
    __tablename__ = "test"
    id = Column(String(255), primary_key=True, index=True, default=UUID_HEX)
    text = Column(String(255), index=True)


class UserCustom(db.Base):
    __tablename__ = "user_custom"
    id = Column(String(255), primary_key=True, index=True, default=uuid4().hex)
    email = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(50))
    phone_country_code = Column(String(7))
    password_hash = Column(Text(), nullable=False)
    image_url = Column(Text())
    device_id = Column(Text())
    google_id = Column(String(255))
    google_image_url = Column(Text())
    is_deleted = Column(Boolean, index=True, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_created_db = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated_db = Column(DateTime, default=datetime.datetime.utcnow)
