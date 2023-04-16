from typing import Annotated
from passlib.context import CryptContext
from fastapi import routing, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import UserInDB, BaseUser, fake_users_db

router = routing.APIRouter(tags=['auth'])


oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.get('/check')
async def check_token(token: Annotated[str, Depends(oauth2_schema)])->dict:
    return {'token': token}



#!---------------------
#! authentication
#!---------------------
def get_user(db, username: str)->UserInDB|None:
    """Get a user from a given DB"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    

def fake_decode_token(token:str)->BaseUser|None:
    """Return a fake decoded token"""
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)]
)->UserInDB:
    """Get current user based on oauth2_scheme"""
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
)->UserInDB:
    """Get current user and verify if it is active"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def fake_hashed_password(password:str)->str:
    """Return Fake Hashed Password"""
    return "fakehashed" + password


@router.get("/user/me")
async def read_users_me(
    current_user: Annotated[BaseUser, Depends(get_current_active_user)]
)->BaseUser:
    return current_user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
)->dict[str, str]:
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}