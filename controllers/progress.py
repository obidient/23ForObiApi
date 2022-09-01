from typing import List
from urllib import response

import fastapi
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter
from models import village_models, voter_models
from utils.progress import calculate_progress_percentage

app = APIRouter()


@app.get("/get-overall-progress-village/{village_id}")
async def get_overall_progress_village(
    village_id: str,
    db: Session = fastapi.Depends(get_db),
):
    response = {
        "number_of_voters": 0,
        "total_number_of_voters_expected": 0,
        "progress_percentage": 0,
    }
    try:
        voters = (
            db.query(voter_models.Voter)
            .filter(voter_models.Voter.village_id == village_id)
            .count()
        )
    except Exception as e:
        raise fastapi.HTTPException(status_code=404, detail=str(e.__str__()))

    response["number_of_voters"] = voters
    response["total_number_of_voters_expected"] = 23
    response["progress_percentage"] = calculate_progress_percentage(voters, 23)
    return response


@app.get("/overall-progress")
async def get_overall_progress(
    db: Session = fastapi.Depends(get_db),
):
    response = {
        "progress_percentage": 0,
        "total_number_of_voters": 0,
    }
    # number of voters
    voters = db.query(voter_models.Voter).count()

    # number of villages
    villages = (db.query(village_models.Village).count()) * 23

    response["progress_percentage"] = calculate_progress_percentage(voters, villages)
    response["total_number_of_voters"] = voters

    return response


@app.get("/statistcis")
async def get_statistics(db: Session = fastapi.Depends(get_db)):
    response = {
        "number_of_voters": 0,
        "number_of_villages": 0,
        "number_of_users": 0,
    }

    # count total number of voters in the database
    voters = db.query(voter_models.Voter).count()
    response["number_of_voters"] = voters

    # count total number of villages in the database
    villages = db.query(village_models.Village).count()
    response["number_of_villages"] = villages

    # count total number of users in the database
    users = db.query(village_models.User).count()
    response["number_of_users"] = users

    return response
