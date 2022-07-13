import json

import pkg_resources
from bigfastapi.schemas.countries_schemas import State
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

app = APIRouter(tags=["States"])

COUNTRIES_DATA_PATH = pkg_resources.resource_filename("bigfastapi", "data/")


@app.get("/{country_code}/states", response_model=State, status_code=200)
def get_country_states(country_code: str):
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
        state["progress"] = 0 
        state["vote_control"] = 0

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
