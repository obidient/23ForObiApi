from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.auth_api import is_authenticated
from bigfastapi.db.database import get_db
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter, Depends
from models.models import UserData
from schemas.schemas import UserDataSchema

app = APIRouter()


@app.post("/user-data")
async def add_user_data(
    user_data: UserDataSchema,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if user already has data
    user_data_exists = db.query(UserData).filter(UserData.user == user.id).first()

    if user_data_exists:
        # update user data
        user_data_exists.data = user_data.data
        db.add(user_data_exists)
        db.commit()
        db.refresh(user_data_exists)

        return {"message": "User data updated"}

    # add new user data
    user_data = UserData(id=uuid4().hex, user=user.id, data=user_data.data)

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return {"message": "User data added"}