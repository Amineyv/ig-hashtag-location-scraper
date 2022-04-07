from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from scrape.main import scrape_graphql, scrape_http
from .token import token_gen

# Theoretical DB
users_db = {
    "amin": {
        "full_name": "Amin Eyvazlou",
        "username": "amin",
        "hashed_password": "hashhash4321",
        "disabled": False,
    },
    "sally": {
        "full_name": "Sally Hoseini",
        "username": "sally",
        "hashed_password": "hashhash1234",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "hashhash" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Models:


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    enabled: Optional[bool] = True


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    """
    Returns the key and value of the users in a dictionary-form argument.
    Like:
        username = user_dict["username"]
        full_name = user_dict["full_name"]
        ...

    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(users_db, token)
    return user


def decode_token(token):
    with open("token.key", "r") as file:
        authentication = file.read()
        file.close()
    return authentication


async def get_current_user(token: str = Depends(oauth2_scheme)):
    passport = decode_token(token)

    if not passport:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return passport


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": token_gen(), "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/")
def index():
    content = {
        "Login": "/login",
        "Logout": "/logout",
        "Hashtag": "/hashtag/{tag}",
        "Location": "/location",
    }

    return content


@app.get("/hashtag/{query}")
def hashtag(query: str, current_user: User = Depends(get_current_active_user)):
    print(query)
    data = scrape_http(query)
    print(data)
    print(data.headers)
    return "OK"


@app.get("/location")
def location(link: str):
    pass
    # TODO


@app.get("/info")
def info(current_user: User = Depends(get_current_active_user)):
    from .settings import Settings

    settings = Settings()
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "users": settings.default_users.keys(),
        "amt_of_posts": settings.default_posts,
    }
