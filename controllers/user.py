from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.auth_api import is_authenticated
from bigfastapi.db.database import get_db
from bigfastapi.models.user_models import User
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter, Depends
from models.village_models import LocalGovernment, LocationCustom, UserData, Village
from schemas.schemas import (
    CreateUserDataSchema,
    UserDataSchema,
    UserSchemaCustom,
    UserUpdateSchema,
)
from schemas.village_schemas import LgaSchema, StateDetails
from schemas.village_schemas import Village as VillageSchema

app = APIRouter()


@app.get("/user-data")
async def get_user_data(
    user: User = Depends(is_authenticated), db: Session = Depends(get_db)
):
    user_data = db.query(UserData).filter(UserData.user == user.id).first()

    if not user_data:
        raise fastapi.HTTPException(
            status_code=400, detail="User data does not exist for this user"
        )
    resp = {
        "user_data": UserDataSchema.from_orm(user_data),
        "state": StateDetails.from_orm(user_data.location),
        "lga": LgaSchema.from_orm(user_data.local_government)
        if user_data.local_government
        else None,
        "village": VillageSchema.from_orm(user_data.village_id),
        "user": UserSchemaCustom.from_orm(user),
    }
    return resp


@app.post("/user-data")
async def add_user_data(
    user_data: CreateUserDataSchema,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if user already has data
    user_data_exists = db.query(UserData).filter(UserData.user == user.id).first()

    information_data = user_data.data

    state_id = information_data.get("state")
    state = db.query(LocationCustom).filter(LocationCustom.id == state_id).first()
    if not state:
        raise fastapi.HTTPException(status_code=404, detail="State does not exist")

    lga_id = information_data.get("lga")
    lga = db.query(LocalGovernment).filter(LocalGovernment.id == lga_id).first()
    if not lga:
        raise fastapi.HTTPException(status_code=404, detail="LGA does not exist")

    if not user_data.is_village_new:
        village_id = information_data.get("village")
        village = db.query(Village).filter(Village.id == village_id).first()
        if not village:
            raise fastapi.HTTPException(
                status_code=404, detail="Village does not exist"
            )
    else:
        # create new village
        village = Village(
            id=uuid4().hex,
            name=information_data.get("village"),
            location=state,
            local_government=lga,
            contributed_by=user.id,
        )
        db.add(village)
        db.commit()
        db.refresh(village)

    # pop village and state from data
    information_data.pop("village")
    information_data.pop("state")
    information_data.pop("lga")

    if user_data_exists:
        # update user data
        user_data_exists.data = information_data
        user_data_exists.village = village.id
        user_data_exists.state = state.id
        user_data_exists.local_government_id = lga.id
        db.add(user_data_exists)
        db.commit()
        db.refresh(user_data_exists)

        resp = {
            "user_data": UserDataSchema.from_orm(user_data_exists),
            "state": StateDetails.from_orm(user_data_exists.location),
            "local_government": LgaSchema.from_orm(user_data_exists.local_government),
            "village": VillageSchema.from_orm(user_data_exists.village_id),
            "user": UserSchemaCustom.from_orm(user),
        }

        return resp

    # add new user data
    user_data = UserData(
        id=uuid4().hex,
        user=user.id,
        data=user_data.data,
        village=village.id,
        local_government_id=lga.id,
        state=state.id,
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    resp = {
        "user_data": UserDataSchema.from_orm(user_data),
        "state": StateDetails.from_orm(user_data.location),
        "local_government": LgaSchema.from_orm(user_data.local_government),
        "village": VillageSchema.from_orm(user_data.village_id),
        "user": UserSchemaCustom.from_orm(user),
    }

    return resp


@app.put("/user-data/{user_data_id}")
async def update_user_data(
    user_data_id: str,
    user_data: CreateUserDataSchema,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if user data exists
    user_data_exists = db.query(UserData).filter(UserData.id == user_data_id).first()

    if not user_data_exists:
        raise fastapi.HTTPException(status_code=400, detail="User data does not exist")

    # update user data
    user_data_exists.data = user_data.data
    db.add(user_data_exists)
    db.commit()
    db.refresh(user_data_exists)

    resp = {
        "user_data": UserDataSchema.from_orm(user_data_exists),
        "state": StateDetails.from_orm(user_data_exists.location),
        "local_government": LgaSchema.from_orm(user_data_exists.local_government),
        "village": VillageSchema.from_orm(user_data_exists.village_id),
        "user": UserSchemaCustom.from_orm(user),
    }

    return resp


@app.get("/user-details", response_model=UserSchemaCustom)
async def get_user_details(
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    user = db.query(User).filter(User.id == user.id).first()

    return UserSchemaCustom.from_orm(user) if user else None


@app.put("/user-details")
async def update_user_details(
    data: UserUpdateSchema,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # get user instance
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise fastapi.HTTPException(status_code=400, detail="User does not exist")

    # get user details instance
    user_details = db.query(UserData).filter(UserData.user == user.id).first()
    if not user_details:
        raise fastapi.HTTPException(status_code=400, detail="User data does not exist")

    # get location instance
    location = db.query(LocationCustom).filter(LocationCustom.id == data.state).first()
    if not location:
        raise fastapi.HTTPException(status_code=400, detail="Location does not exist")

    # get village instance
    village = db.query(Village).filter(Village.id == data.village).first()
    if not village:
        raise fastapi.HTTPException(status_code=400, detail="Village does not exist")

    try:
        user.first_name = data.firstname
        user.last_name = data.lastname
        # user.email = data.email
        db.add(user)
        db.commit()
        db.refresh(user)

        user_details.state = location.id
        user_details.village = village.id
        user_details.local_government_id = village.local_government
        db.add(user_details)
        db.commit()
        db.refresh(user_details)
    except Exception as err:
        raise fastapi.HTTPException(status_code=400, detail=str(err))

    resp = {
        "user_data": UserDataSchema.from_orm(user_details),
        "state": StateDetails.from_orm(user_details.location),
        "village": VillageSchema.from_orm(user_details.village_id),
        "user": UserSchemaCustom.from_orm(user),
    }

    return resp
