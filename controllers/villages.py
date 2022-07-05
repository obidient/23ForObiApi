from typing import List

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter
from models import village_models
from schemas import village_schemas

app = APIRouter()


@app.get("/villages/{state_code}", response_model=List[village_schemas.Village])
async def list_villages_in_a_state(
    state_code: str, db: Session = fastapi.Depends(get_db)
):
    villages = db.query(village_models.Village).filter(
        village_models.Village.location == state_code
    )

    return list(map(village_schemas.Village.from_orm, villages))

# @app.get("/village-details")