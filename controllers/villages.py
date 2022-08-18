from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.auth_api import is_authenticated
from bigfastapi.db.database import get_db
from bigfastapi.models import user_models
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter, Depends
from models import village_models
from schemas import village_schemas
from utils.progress import calculate_progress_percentage, top_contributors_in_a_village

app = APIRouter()


@app.get("/state-details/{state_code}", response_model=village_schemas.StateDetails)
async def get_state_details(state_code: str, db: Session = fastapi.Depends(get_db)):
    state_details = (
        db.query(village_models.LocationCustom)
        .filter(village_models.LocationCustom.id == state_code)
        .first()
    )

    if not state_details:
        raise fastapi.HTTPException(status_code=404, detail="State not found")

    return village_schemas.StateDetails.from_orm(state_details)


@app.post("/villages")
async def create_village(
    village: village_schemas.VillageBase,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # get location
    location = db.query(village_models.LocationCustom).get(village.location_id)

    db_village = village_models.Village(
        id=uuid4().hex,
        name=village.name,
        location=location,
        contributed_by=user.id,
    )
    try:
        db.add(db_village)
        db.commit()
        db.refresh(db_village)
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e.__str__()))

    return {
        "message": "Village created succesfully",
        "village": village_schemas.Village.from_orm(db_village),
    }


@app.get("/villages/{state_code}")
async def list_villages_in_a_state(
    state_code: str, db: Session = fastapi.Depends(get_db)
):
    villages = (
        db.query(village_models.Village)
        .options(Session.lazyload(village_models.Village.voters))
        .filter(
            village_models.Village.location_id == state_code,
            village_models.Village.is_active == True,
        )
    )

    if len(list((villages))) == 0:
        return []

    resp = {"list_of_villages": []}
    state_vote_count = 0
    number_of_villages = (villages.count()) * 23
    for village in villages:
        top_five = top_contributors_in_a_village(village.voters)

        top_five_details = [
            users_schemas.User.from_orm(db.query(user_models.User).get(x))
            for x in top_five
            if x is not None
        ]

        voters_per_village = len(village.voters)
        state_vote_count += voters_per_village
        resp["list_of_villages"].append(
            {
                "id": village.id,
                "name": village.name,
                "state": village.location,
                "contributed_by": village.contributed_by,
                "voters": voters_per_village,
                "progress_percentage": calculate_progress_percentage(
                    voters_per_village
                ),
                "top_contributors": top_five_details,
            }
        )

    resp["villages_in_control"] = calculate_progress_percentage(
        state_vote_count, number_of_villages
    )
    return resp


@app.get("/village-details/{village_id}")
async def get_village_details(village_id: str, db: Session = fastapi.Depends(get_db)):
    village = (
        db.query(village_models.Village)
        .options(Session.lazyload(village_models.Village.voters))
        .filter(village_models.Village.id == village_id)
        .first()
    )

    if not village:
        raise fastapi.HTTPException(status_code=404, detail="Village not found")

    top_five = top_contributors_in_a_village(village.voters)

    top_five_details = [
        users_schemas.User.from_orm(db.query(user_models.User).get(x))
        for x in top_five
        if x is not None
    ]

    resp = {
        "id": village.id,
        "name": village.name,
        "state": village.location,
        "contributed_by": village.contributed_by,
        "voters": len(village.voters),
        "progress_percentage": calculate_progress_percentage(len(village.voters)),
        "top_contributors": top_five_details,
    }

    return resp


@app.get(
    "/village-by-contributors/{contributor_id}",
    response_model=List[village_schemas.Village],
)
async def get_villages_by_contributor(
    contributor_id: str, db: Session = fastapi.Depends(get_db)
):
    villages = db.query(village_models.Village).filter(
        village_models.Village.contributed_by == contributor_id,
        village_models.Village.is_active == True,
    )

    return list(map(village_schemas.Village.from_orm, villages))


@app.get("/village-search/{search_term}", response_model=List[village_schemas.Village])
async def search_villages(search_term: str, db: Session = fastapi.Depends(get_db)):
    villages = db.query(village_models.Village).filter(
        village_models.Village.name.ilike("%" + search_term + "%")
    )

    return list(map(village_schemas.Village.from_orm, villages))


@app.post("/user-villages")
async def add_user_village(
    user_village: village_schemas.UserVillageBase,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if village exists
    village_obj = db.query(village_models.Village).get(user_village.village_id)
    if not village_obj:
        raise fastapi.HTTPException(status_code=404, detail="Village not found")

    # check if user already added this village
    user_village_exists = (
        db.query(village_models.UserVillage)
        .filter(
            village_models.UserVillage.user == user.id,
            village_models.UserVillage.village_id == village_obj.id,
        )
        .first()
    )

    if user_village_exists:
        raise fastapi.HTTPException(
            status_code=400, detail="User already added this village"
        )

    try:
        # add user to village
        db_user_village = village_models.UserVillage(
            id=uuid4().hex,
            user=user.id,
            village_id=village_obj.id,
            state_id=village_obj.location_id,
        )
        db.add(db_user_village)
        db.commit()
        db.refresh(db_user_village)
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e.__str__()))

    return {
        "message": "User added to village succesfully",
    }


@app.get("/user-villages")
async def get_user_villages(
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    user_villages = (
        db.query(village_models.UserVillage)
        .options(Session.lazyload(village_models.UserVillage.village))
        .filter(village_models.UserVillage.user == user.id)
    )

    if len(list((user_villages))) == 0:
        return []

    resp = []

    for user_village in user_villages:
        resp.append(
            {
                "id": user_village.id,
                "village": user_village.village,
            }
        )

    return resp
