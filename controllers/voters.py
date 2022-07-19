from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter
from models import village_models, voter_models
from schemas import voter_schemas

app = APIRouter()


@app.get("/voters/{village_id}", response_model=List[voter_schemas.VoterSchema])
async def list_voters_in_a_village(
    village_id: str, db: Session = fastapi.Depends(get_db)
):
    voters = db.query(voter_models.Voter).filter(
        voter_models.Voter.village_id == village_id
    )

    return list(map(voter_schemas.VoterSchema.from_orm, voters))


@app.post("/voters")
async def add_voters_to_village(
    voter: voter_schemas.VoterSchemaBase, db: Session = fastapi.Depends(get_db)
):
    # check if village exist
    village = db.query(village_models.Village).get(voter.village_id)
    if not village:
        raise fastapi.HTTPException(status_code=400, detail="Village does not exist")

    db_voters_to_village = voter_models.Voter(
        id=uuid4().hex,
        name=voter.name,
        village=village,
        contact=voter.contact,
        notes=voter.notes,
        importance=voter.importance
    )

    db.add(db_voters_to_village)
    db.commit()
    db.refresh(db_voters_to_village)
    return {
        "message": "Support Group created succesfully",
        "support_group": voter_schemas.VoterSchema.from_orm(db_voters_to_village),
    }
