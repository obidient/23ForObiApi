from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter
from models import village_models, voter_models
from schemas import village_schemas
from utils.progress import calculate_progress_percentage

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
    village: village_schemas.VillageBase, db: Session = fastapi.Depends(get_db)
):
    # get location
    location = db.query(village_models.LocationCustom).get(village.location_id)

    db_village = village_models.Village(
        id=uuid4().hex,
        name=village.name,
        location=location,
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
        .filter(village_models.Village.location_id == state_code)
    )

    if len(list((villages))) == 0:
        raise fastapi.HTTPException(status_code=404, detail="Village(s) not found")

    resp = {"list_of_villages": []}
    state_vote_count = 0
    number_of_villages = (villages.count()) * 23
    for village in villages:
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
                "top_contributors": [],
            }
        )
    resp["villages_in_control"] = calculate_progress_percentage(
        state_vote_count, number_of_villages
    )
    return resp


@app.get("/village-details/{village_id}", response_model=village_schemas.Village)
async def get_village_details(village_id: str, db: Session = fastapi.Depends(get_db)):
    village = (
        db.query(village_models.Village)
        .filter(village_models.Village.id == village_id)
        .first()
    )

    if not village:
        raise fastapi.HTTPException(status_code=404, detail="Village not found")

    return village_schemas.Village.from_orm(village)


@app.get(
    "/village-by-contributors/{contributor_id}",
    response_model=List[village_schemas.Village],
)
async def get_villages_by_contributor(
    contributor_id: str, db: Session = fastapi.Depends(get_db)
):
    villages = db.query(village_models.Village).filter(
        village_models.Village.contributed_by == contributor_id
    )

    return list(map(village_schemas.Village.from_orm, villages))


@app.get("/village-search/{search_term}", response_model=List[village_schemas.Village])
async def search_villages(search_term: str, db: Session = fastapi.Depends(get_db)):
    villages = db.query(village_models.Village).filter(
        village_models.Village.name.ilike("%" + search_term + "%")
    )

    return list(map(village_schemas.Village.from_orm, villages))


@app.get("/user-villages/{user_id}", response_model=List[village_schemas.UserVillage])
async def get_user_villages(user_id: str, db: Session = fastapi.Depends(get_db)):
    user_villages = db.query(village_models.UserVillage).filter(
        village_models.UserVillage.user_id == user_id
    )

    return list(map(village_schemas.UserVillage.from_orm, user_villages))
