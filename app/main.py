from uuid import UUID
from typing import Annotated
from fastapi import FastAPI, Query, Path, Body, Header
from app.models import (
    Item, DrinkType, DrinkMaster, DrinkType, Maker,
    fake_drink_db, fake_maker_db,
    UserIn, UserOut, UserInDB, BaseUser)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(
    item_id: Annotated[UUID, Path(title="OK", description="item ID")], 
    q: Annotated[
        str | None,
        Query(
            title="Query string!",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None
):
    return {"item_id": item_id, "q": q}


@app.get("/header")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/maker")
async def get_makers(skip: int = 0, limit: int = 10)->list[Maker]:
    """You can get the maker list"""
    return fake_maker_db[skip: skip + limit]


@app.get("/drink")
async def get_drinks(skip: int = 0, limit: int = 10)->list[DrinkMaster]:
    """You can get the drink list"""
    return fake_drink_db[skip: skip + limit]


@app.post("/drink")
async def create_drink(
    drink_master: Annotated[DrinkMaster, Body(description="New DrinkMaster")]
):
    """Create a new drink master"""
    return {"drink_master": drink_master, "message": "created"}


@app.get("/drink/{drink_id}")
async def get_drink(drink_id: int, q2:str, q: str|None = None):
    return {"drink": fake_drink_db[drink_id], "q": q, "q2": q2}


@app.get("/drink/{drink_type}")
async def get_drink_type(drink_type: DrinkType):
    if drink_type is DrinkType.BEER:
        return {"drink_type": drink_type, "message": "You should visit a brewery !"}
    elif drink_type is DrinkType.WINE:
        return {"drink_type": drink_type, "message": "California is the best place for wine lovers !"}
    elif drink_type is DrinkType.SAKE:
        return {"drink_type": drink_type, "message": "Sake is a Japanese treasure !"}
    return {"drink_type": drink_type, "message": "Not sure what it is ... ?"}



def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print(f"Input data: {user_in.dict()}")
    print(f"User saved! ..not really: {user_in_db}")
    return user_in_db


@app.post("/user/")
async def create_user(user_in: UserIn)->UserOut:
    user_saved = fake_save_user(user_in)
    return user_saved