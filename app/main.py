from enum import Enum
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

class DrinkType(str, Enum):
    BEER = "beer"
    WINE = "wine"
    SAKE = "sake"

fake_drink_db = [
    {"name": "TAHOE DEEP", "type": DrinkType.BEER},
    {"name": "Faction Pale", "type": DrinkType.BEER},
    {"name": "Chardonnay", "type": DrinkType.WINE},
    {"name": "Cabernet Sauvignon", "type": DrinkType.WINE},
    {"name": "一ノ蔵 辛口", "type": DrinkType.SAKE},
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/drink")
async def get_drinks(skip: int = 0, limit: int = 10):
    """You can get the drink list"""
    return fake_drink_db[skip: skip + limit]


@app.get("/drink/{drink_id}")
async def get_drink(drink_id: int, q2:str, q: Union[str, None] = None):
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

