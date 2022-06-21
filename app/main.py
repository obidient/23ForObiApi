import bigfastapi
import database
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bigfastapi.countries import app as countries
from api import app as api

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(countries, tags=["Countries"])
app.include_router(api,  tags=["Api"])

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
    uvicorn.run("main:app", port=7001, reload=True)