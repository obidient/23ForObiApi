import fastapi, os
import sqlalchemy.orm as orm
import schemas.schemas as schemas
import models as models

from fastapi import FastAPI, status, APIRouter, Depends
from database.db import get_db

app = APIRouter()

# Return the app version
@app.get("/api/version")
def get_version():
    return "0.1"

# Test a request from the db
@app.post("/api/test_db")
def create_newfollow(body: schemas.TestSchema, db: orm.Session = fastapi.Depends(get_db)):
    return "This will retrieve from the test db"