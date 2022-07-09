from typing import List

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter
from models import village_models
from schemas import village_schemas

app = APIRouter()


@app.get("/state-details/{state_code}", response_model=village_schemas.StateDetails)
async def get_state_details(state_code: str, db: Session = fastapi.Depends(get_db)):
    state_details = db.query(village_models.StateDetails).filter(
        village_models.StateDetails.state_code == state_code
    ).first()

    if not state_details:
        raise fastapi.HTTPException(status_code=404, detail="State not found")
    
    return village_schemas.StateDetails.from_orm(state_details)


@app.post("/villages/")
async def create_village(
    village: village_schemas.VillageBase, db: Session = fastapi.Depends(get_db)
):
    db_village = village_models.Village(
        name=village.name, location=village.location, contributed_by="None"
    )
    db.add(db_village)
    db.commit()
    db.refresh(db_village)
    return {
        "message": "Village created succesfully",
        "village": village_schemas.Village.from_orm(db_village),
    }


@app.get("/villages/{state_code}", response_model=List[village_schemas.Village])
async def list_villages_in_a_state(
    state_code: str, db: Session = fastapi.Depends(get_db)
):
    villages = db.query(village_models.Village).filter(
        village_models.Village.location == state_code
    )

    return list(map(village_schemas.Village.from_orm, villages))


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
async def search_villages(
    search_term: str, db: Session = fastapi.Depends(get_db)
):
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