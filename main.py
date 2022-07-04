import bigfastapi
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from controllers.support_group import app as support_group
from decouple import config
import database
from api import app as api

############IMPORTS FROM BIGFASTAPI#####################
from bigfastapi.countries import app as countries
from bigfastapi.google_auth import app as auth
from bigfastapi.organization import app as organization

PORT = int(config("PORT"))
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="super_secret_key")

app.include_router(countries, tags=["Countries"])
app.include_router(api, tags=["Api"])
app.include_router(support_group, tags=["Support Group"])
app.include_router(auth) #social auth
# app.include_router(organization, tags=["Organization"])

# Create all database objects
database.db.create_database()


@app.get("/", tags=["Home"])
async def get_root() -> dict:
    return {
        "message": "Welcome to BigFastAPI. This is an example of an API built using BigFastAPI.",
        "url": "http://127.0.0.1:7001/docs",
        "api test": "http://127.0.0.1:7001/api/version",
        "add to db": "http://127.0.0.1:7001/api/test_db_add",
        "retrieve from db": "http://127.0.0.1:7001/api/test_db_read",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
