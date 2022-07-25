from typing import List
from uuid import uuid4

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter
from models import support_group_models
from schemas import support_group_schemas

app = APIRouter()


@app.post("/support-group/")
async def create_support_group(
    support_group: support_group_schemas.SupportGroupBase,
    db: Session = fastapi.Depends(get_db),
):
    db_support_group = support_group_models.SupportGroup(
        id=uuid4().hex,
        name=support_group.name,
        votes_delivered=support_group.votes_delivered,
    )
    db.add(db_support_group)
    db.commit()
    db.refresh(db_support_group)
    return {
        "message": "Support Group created succesfully",
        "support_group": support_group_schemas.SupportGroup.from_orm(db_support_group),
    }


@app.get("/support-group/", response_model=List[support_group_schemas.SupportGroup])
async def get_support_group(db: Session = fastapi.Depends(get_db)):
    support_group = (
        db.query(support_group_models.SupportGroup)
        .filter(support_group_models.SupportGroup.is_active == True)
        .all()
    )
    return list(map(support_group_schemas.SupportGroup.from_orm, support_group))


@app.get(
    "/support-group/{support_group_id}",
    response_model=support_group_schemas.SupportGroup,
)
def get_support_group_by_id(
    support_group_id: str, db: Session = fastapi.Depends(get_db)
):
    support_group = (
        db.query(support_group_models.SupportGroup)
        .filter(support_group_models.SupportGroup.id == support_group_id)
        .first()
    )
    if not support_group:
        raise fastapi.HTTPException(status_code=404, detail="Support Group not found")

    return support_group_schemas.SupportGroup.from_orm(support_group)
