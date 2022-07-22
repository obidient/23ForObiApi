import json
from typing import List

import fastapi
import pkg_resources
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.village_models import LocationCustom
from schemas.village_schemas import StateDetails
from utils.progress import calculate_progress_percentage

app = APIRouter(tags=["States"])

COUNTRIES_DATA_PATH = pkg_resources.resource_filename("bigfastapi", "data/")


@app.get("/...")
def testss(db: Session = fastapi.Depends(get_db)):
    country_code = "NG"
    country_data = []
    with open(COUNTRIES_DATA_PATH + "/countries.json") as file:
        countries = json.load(file)
        country_data = list(
            filter(
                lambda data: data["iso2"].casefold() == country_code.casefold()
                or data["iso3"].casefold() == country_code.casefold(),
                countries,
            )
        )
        if not country_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
            )
        data = country_data[0]
        del data["dial_code"]
        del data["sample_phone_format"]

    # add progress and vote control keys to each state
    for state in data["states"]:
        try:
            loc = LocationCustom(
                id=state["state_code"],
                country=data["name"],
                state_name=state["name"],
            )
            db.merge(loc)
            db.commit()
            db.refresh(loc)
        except Exception as e:
            print(str(e))
            pass


@app.get("/states", response_model=List[StateDetails])
def get_country_states(db: Session = fastapi.Depends(get_db)):
    all_states = (
        db.query(LocationCustom).options(Session.lazyload(LocationCustom.village)).all()
    )

    for state in all_states:
        number_of_voters = 0
        number_of_villages = len(state.village) * 23
        for village in state.village:
            number_of_voters += len(village.voters)
        state.progress = calculate_progress_percentage(
            number_of_voters, number_of_villages
        )
        state.vote_control = state.progress
    return [StateDetails.from_orm(state) for state in all_states]
