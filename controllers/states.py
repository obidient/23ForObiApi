import json
from uuid import uuid4

import fastapi
import pkg_resources
import sqlalchemy.orm as Session
from bigfastapi.db.database import get_db
from models.village_models import LocationCustom
from bigfastapi.schemas.countries_schemas import State
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

app = APIRouter(tags=["States"])

COUNTRIES_DATA_PATH = pkg_resources.resource_filename("bigfastapi", "data/")


@app.get("/{country_code}/states", response_model=State, status_code=200)
def get_country_states(country_code: str, db: Session = fastapi.Depends(get_db)):
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
            )
            db.merge(loc)
            db.commit()
            db.refresh(loc)
        except Exception as e:
            print(str(e))
            pass

        state["progress"] = 0
        state["vote_control"] = 0

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
