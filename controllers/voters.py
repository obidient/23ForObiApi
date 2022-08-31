from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.auth_api import is_authenticated
from bigfastapi.db.database import get_db
from bigfastapi.schemas import users_schemas
from fastapi import APIRouter, Depends
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


@app.get("/voters-by-contributor")
async def list_voters_by_contributor(
    db: Session = fastapi.Depends(get_db),
    user: users_schemas.User = Depends(is_authenticated),
):
    voters = (
        db.query(voter_models.Voter)
        .options(Session.lazyload(voter_models.Voter.village))
        .filter(voter_models.Voter.delivered_by == user.id)
    )

    if voters == []:
        raise fastapi.HTTPException(status_code=404, detail="No voters found")

    resp = []
    for voter in voters:
        resp.append(
            {
                "id": voter.id,
                "name": voter.name,
                "village": voter.village,
                "contact": voter.contact,
                "notes": voter.notes,
                "importance": voter.importance,
            }
        )
    return resp


@app.post("/voters")
async def add_voters_to_village(
    voter: voter_schemas.VoterSchemaBase,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if village exist
    village = db.query(village_models.Village).get(voter.village_id)
    if not village:
        raise fastapi.HTTPException(status_code=400, detail="Village does not exist")

    
    # check if voter already exists
    if voter.contact != "" and voter.contact != None:
        voter_exists = (
            db.query(voter_models.Voter)
            .filter(voter_models.Voter.contact == voter.contact)
            .first()
        )
        if voter_exists:
            raise fastapi.HTTPException(status_code=400, detail="Voter already exists")

    db_voters_to_village = voter_models.Voter(
        id=uuid4().hex,
        name=voter.name,
        village=village,
        contact=voter.contact,
        notes=voter.notes,
        importance=voter.importance,
        delivered_by=user.id,
    )

    db.add(db_voters_to_village)
    db.commit()
    db.refresh(db_voters_to_village)
    return {
        "message": "Voter created succesfully",
        "support_group": voter_schemas.VoterSchema.from_orm(db_voters_to_village),
    }


@app.put("/voters/{voter_id}")
async def update_voter(
    voter_id: str,
    voter: voter_schemas.VoterSchemaBase,
    user: users_schemas.User = Depends(is_authenticated),
    db: Session = fastapi.Depends(get_db),
):
    # check if village exist
    village = db.query(village_models.Village).get(voter.village_id)
    if not village:
        raise fastapi.HTTPException(status_code=400, detail="Village does not exist")

    db_voter = db.query(voter_models.Voter).get(voter_id)
    if not db_voter:
        raise fastapi.HTTPException(status_code=404, detail="Voter does not exist")

    db_voter.name = voter.name
    db_voter.village = village
    db_voter.contact = voter.contact
    db_voter.notes = voter.notes
    db_voter.importance = voter.importance
    db_voter.delivered_by = user.id

    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return {
        "message": "Voter updated succesfully",
        "support_group": voter_schemas.VoterSchema.from_orm(db_voter),
    }
