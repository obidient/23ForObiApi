from uuid import uuid4

import fastapi
import sqlalchemy.orm as orm
from fastapi import APIRouter, Depends, FastAPI, status

import models.models as models
import schemas.schemas as schemas
from database.db import get_db

app = APIRouter()


# Return the app version
@app.get("/api/version")
def get_version():
    return "0.1"


# Test a request from the db
@app.get("/api/test_db_read")
def test_db_read(db: orm.Session = fastapi.Depends(get_db)):
    object = db.query(models.Test).all()
    if object:
        return {"status": True, "data": object}
    else:
        return "DoesNotExist"


# Test add a request to the db
@app.get("/api/test_db_add")
def test_db_add(db: orm.Session = fastapi.Depends(get_db)):

    obj = models.Test(id=uuid4().hex, text="Added Data: " + uuid4().hex)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return schemas.TestSchema.from_orm(obj)
