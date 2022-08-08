import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import database
from api import app as api
from controllers.user import app as user_data
from controllers.campaign_images import app as campaign_image
from controllers.google_auth import app as google_auth
from controllers.progress import app as progress
from controllers.states import app as states
from controllers.support_group import app as support_group
from controllers.villages import app as villages
from controllers.voters import app as voters

app = FastAPI()

BASE_URL = config("BASE_URL")
PORT = int(config("PORT"))

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="maihoonjiyan")

app.include_router(api, tags=["Api"])
app.include_router(campaign_image, tags=["Campaign Images"])
app.include_router(google_auth, tags=["Google Auth"])
app.include_router(progress, tags=["Progress"])
app.include_router(states, tags=["States"])
app.include_router(support_group, tags=["Support Group"])
app.include_router(user_data, tags=["User Data"])
app.include_router(villages, tags=["Villages"])
app.include_router(voters, tags=["Voters"])

# Create all database objects
database.db.create_database()


@app.get("/", tags=["Home"])
async def get_root() -> dict:
    return {
        "message": "Welcome to BigFastAPI. This is an example of an API built using BigFastAPI.",
        "url": f"{BASE_URL}/docs",
        "api test": f"{BASE_URL}/api/version",
        "add to db": f"{BASE_URL}/api/test_db_add",
        "retrieve from db": f"{BASE_URL}/api/test_db_read",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
