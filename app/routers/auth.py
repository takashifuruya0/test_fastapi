from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import routing, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserInDB, BaseUser, Token, TokenData, fake_users_db

router = routing.APIRouter(tags=['auth'])

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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


async def get_current_user(token: Annotated[str, Depends(oauth2_schema)])->UserInDB:
    """Get current user based on oauth2_scheme"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
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


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password:str):
    return pwd_context.hash(plain_password)


def authenticate_user(fake_db, username:str, plain_password:str)->UserInDB|None:
    user = get_user(fake_db, username)
    if not user:
        return 
    if not verify_password(plain_password, user.hashed_password):
        return 
    return user


def create_access_token(data:dict, expires_delta:timedelta|None=None)->str:
    """Create Access Token

    Args:
        data (dict): data to be encoded
        expires_delta (timedelta|None): By default is None.
    Returns:
        str: jwt token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/user/me")
async def read_users_me(
    current_user: Annotated[BaseUser, Depends(get_current_active_user)]
)->BaseUser:
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
)->dict[str, str]:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}