from typing import List

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter
from models import voter_models
from utils.progress import calculate_progress_percentage

app = APIRouter()


@app.post("/get-overall-progress-village/{village_id}")
async def get_overall_progress_village(
    village_id: str,
    db: Session = fastapi.Depends(get_db),
):
    response = {
        "number_of_voters": 0,
        "total_number_of_voters_expected": 0,
        "progress_percentage": 0,
    }
    voters = (
        db.query(voter_models.Voter)
        .filter(voter_models.Voter.village == village_id)
        .count()
    )
    response["number_of_voters"] = voters
    response["total_number_of_voters_expected"] = 23
    response["progress_percentage"] = calculate_progress_percentage(voters, 23)
    return response
