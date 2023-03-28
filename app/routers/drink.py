from typing import Annotated
from fastapi import Body, status, routing
from app.models import (
    Item, DrinkType, DrinkMaster, DrinkType, Maker,
    fake_drink_db, fake_maker_db)


router = routing.APIRouter(tags=["drink", ])



@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@router.get("/maker")
async def get_makers(skip: int = 0, limit: int = 10)->list[Maker]:
    """You can get the maker list"""
    return fake_maker_db[skip: skip + limit]


@router.get("/drink")
async def get_drinks(skip: int = 0, limit: int = 10)->list[DrinkMaster]:
    """You can get the drink list"""
    return fake_drink_db[skip: skip + limit]


@router.post("/drink", status_code=status.HTTP_201_CREATED)
async def create_drink(
    drink_master: Annotated[DrinkMaster, Body(description="New DrinkMaster")]
):
    """Create a new drink master"""
    return {"drink_master": drink_master, "message": "created"}


@router.get("/drink/{drink_id}")
async def get_drink(drink_id: int, q2:str, q: str|None = None):
    return {"drink": fake_drink_db[drink_id], "q": q, "q2": q2}


@router.get("/drink/{drink_type}")
async def get_drink_type(drink_type: DrinkType):
    if drink_type is DrinkType.BEER:
        return {"drink_type": drink_type, "message": "You should visit a brewery !"}
    elif drink_type is DrinkType.WINE:
        return {"drink_type": drink_type, "message": "California is the best place for wine lovers !"}
    elif drink_type is DrinkType.SAKE:
        return {"drink_type": drink_type, "message": "Sake is a Japanese treasure !"}
    return {"drink_type": drink_type, "message": "Not sure what it is ... ?"}

