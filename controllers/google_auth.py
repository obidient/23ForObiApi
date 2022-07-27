import random
import string
from multiprocessing.spawn import import_main_path
from uuid import uuid4

import fastapi
import passlib.hash as _hash
import sqlalchemy.orm as orm
from authlib.integrations.starlette_client import OAuth
from bigfastapi.auth_api import create_access_token
from bigfastapi.db.database import get_db
from bigfastapi.models.organization_models import Organization
from bigfastapi.models.user_models import User
from bigfastapi.schemas.users_schemas import User as UserSchema
from bigfastapi.utils import settings
from fastapi import APIRouter, HTTPException, Request, status
from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.config import Config
from schemas.schemas import GoogleToken

app = APIRouter()


# OAuth settings
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException("Missing env variables")

# Set up OAuth
config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Set up the middleware to read the request session
SECRET_KEY = settings.JWT_SECRET
BASE_URL = settings.BASE_URL

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Google oauth error",
    headers={"WWW-Authenticate": "Bearer"},
)


@app.post("/google/token")
async def google_auth(token: GoogleToken, db: orm.Session = fastapi.Depends(get_db)):
    try:
        user_data = id_token.verify_oauth2_token(
            token.token, requests.Request(), GOOGLE_CLIENT_ID
        )
        check_user = valid_email_from_db(user_data["email"], db)

    except Exception as e:
        print(str(e.__str__()))
        raise CREDENTIALS_EXCEPTION

    if check_user:
        user_id = check_user
        access_token = await create_access_token(data={"user_id": check_user.id}, db=db)
        response = {
            "access_token": access_token,
            "user": UserSchema.from_orm(user_id),
        }
        return response

    S = 10
    ran = "".join(random.choices(string.ascii_uppercase + string.digits, k=S))
    n = str(ran)

    user_obj = User(
        id=uuid4().hex,
        email=user_data["email"],
        first_name=user_data["given_name"],
        last_name=user_data["family_name"],
        password_hash=_hash.sha256_crypt.hash(n),
        phone_number=n,
        is_active=True,
        is_verified=True,
        is_deleted=False,
        google_id="",
        google_image_url=user_data["picture"],
        image_url=user_data["picture"],
        device_id="",
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    access_token = await create_access_token(data={"user_id": user_obj.id}, db=db)

    response = {
        "access_token": access_token,
        "user": UserSchema.from_orm(user_obj),
    }
    return response


def valid_email_from_db(email, db: orm.Session = fastapi.Depends(get_db)):
    found_user = db.query(User).filter(User.email == email).first()
    return found_user
