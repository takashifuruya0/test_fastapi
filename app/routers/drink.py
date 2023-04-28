from typing import Annotated
from fastapi import Body, status, routing
from fastapi.encoders import jsonable_encoder
from depends import CommonsDep
from models import (
    DrinkType, DrinkMaster, DrinkType, Maker,
    DrinkReview, fake_review_db,
    fake_drink_db, fake_maker_db)


router = routing.APIRouter(tags=["drink", ])


#!--------------------------------
#! Maker
#!--------------------------------
@router.get("/maker")
async def list_makers(commons: CommonsDep)->list[Maker]:
    """You can get the maker list"""
    return fake_maker_db[commons.skip: commons.skip + commons.limit]
    


#!--------------------------------
#! Drink
#!--------------------------------
@router.get("/drink")
async def list_drinks(commons: CommonsDep)->list[DrinkMaster]:
    """You can get the drink list"""
    return fake_drink_db[commons.skip: commons.skip + commons.limit]


@router.post("/drink", status_code=status.HTTP_201_CREATED)
async def create_drink(
    drink_master: Annotated[DrinkMaster, Body(description="New DrinkMaster")]
):
    """Create a new drink master"""
    return {"drink_master": drink_master, "message": "created"}


@router.get("/drink/{drink_id}")
async def get_drink(drink_id: int, q2:str, q: str|None = None):
    return {"drink": fake_drink_db[drink_id], "q": q, "q2": q2}


@router.put("/drink/{drinkid}")
async def update_drink(drink_id: int, drink_master: DrinkMaster)->DrinkMaster:
    # existing data
    stored_drink_master_model = fake_drink_db[drink_id]
    # update
    update_data = drink_master.dict(exclude_unset=True)
    updated_item = stored_drink_master_model.copy(update=update_data)
    fake_drink_db[drink_id] = jsonable_encoder(updated_item)
    # return
    return updated_item

#!--------------------------------
#! DrinkTYpe
#!--------------------------------
@router.get("/drink/{drink_type}")
async def get_drink_type(drink_type: DrinkType):
    if drink_type is DrinkType.BEER:
        return {"drink_type": drink_type, "message": "You should visit a brewery !"}
    elif drink_type is DrinkType.WINE:
        return {"drink_type": drink_type, "message": "California is the best place for wine lovers !"}
    elif drink_type is DrinkType.SAKE:
        return {"drink_type": drink_type, "message": "Sake is a Japanese treasure !"}
    return {"drink_type": drink_type, "message": "Not sure what it is ... ?"}


#!--------------------------------
#! Review
#!--------------------------------
@router.get("/review")
async def list_reviews(commons: CommonsDep)->list[DrinkReview]:
    return fake_review_db[commons.skip: commons.skip+commons.limit]


@router.get("/review/{review_id}")
async def get_review(review_id:int)->DrinkReview|None:
    return fake_review_db[review_id]
