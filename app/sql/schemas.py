from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from datetime import date


#! ----------------------------
#! Choices
#! ----------------------------
class DrinkType(str, Enum):
    BEER = "beer"
    WINE = "wine"
    SAKE = "sake"


#! ----------------------------
#! Models
#! ----------------------------
#?------------------
#? Maker
#?------------------
class Maker(BaseModel):
    name: str
    state: str = Field(example="California")
    country: str = Field(example="United States")
    description: str
    is_active: bool = True

    class Config:
        orm_mode = True


class MakerCreate(Maker):
    pass


class MakerResponse(Maker):
    id: int


#?------------------
#? Beer
#?------------------
class Beer(BaseModel):
    is_active: bool 
    name: str
    description: str
    ibu: int|None
    abv: float|None

    class Config:
        orm_mode = True


class BeerCreate(Beer):
    maker_id: int


class BeerResponse(Beer):
    id: int
    maker: MakerResponse