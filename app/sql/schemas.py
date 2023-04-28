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


class BeerStyle(str, Enum):
    DEFAULT = '-'
    # IPA
    IPA = "IPA"
    DIPA = "Double IPA"
    TIPA = "Triple IPA"
    # WC
    WC_IPA = 'West Coast IPA'
    WC_DIPA = "Double West Coast IPA"
    WC_TIPA = "Triple West Coast IPA"
    # Hazy
    HZ_IPA = "Hazy IPA"
    HZ_DIPA = 'Double Hazy IPA'
    HZ_TIPA = 'Triple Hazy IPA'
    # Ale
    PALE_ALE = "Pale Ale"
    GOLDEN_ALE = 'Golden Ale'
    # Lager
    PILSNER = 'Pilsner'


#! ----------------------------
#! Models
#! ----------------------------
#?------------------
#? Base
#?------------------
class Maker(BaseModel):
    is_active: bool
    name: str
    description: str
    state: str = Field(example="California")
    country: str = Field(example="United States")
    
    class Config:
        orm_mode = True


class Beer(BaseModel):
    is_active: bool 
    name: str
    description: str
    ibu: int|None
    abv: float|None
    style: BeerStyle = BeerStyle.DEFAULT

    class Config:
        orm_mode = True


class Hops(BaseModel):
    is_active: bool 
    name: str
    description: str|None = None

    class Config:
        orm_mode = True


#?------------------
#? Create
#?------------------
class HopsCreate(Hops):
    pass


class MakerCreate(Maker):
    pass


class BeerCreate(Beer):
    maker_id: int


#?------------------
#? Response
#?------------------
class HopsResponse(Hops):
    id: int


class MakerResponse(Maker):
    id: int
    beers: list[Beer]


class BeerResponse(Beer):
    id: int
    maker: MakerResponse
    hops: list[HopsResponse]
