from typing import Annotated
from fastapi import Form, status, routing
from app.models import UserIn, UserOut, UserInDB


router = routing.APIRouter(tags=["user", ])


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print(f"Input data: {user_in.dict()}")
    print(f"User saved! ..not really: {user_in_db}")
    return user_in_db


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn)->UserOut:
    user_saved = fake_save_user(user_in)
    return user_saved


@router.post("/login/")
async def login(
    username: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    password: Annotated[str, Form()]
) -> UserOut:
    """Login Form"""
    hashed_password = fake_password_hasher(password)
    return {"username": username, "email": email, "hashed_password": hashed_password}