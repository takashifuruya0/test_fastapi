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


class Purchase(BaseModel):
    is_active: bool
    description: str|None = None
    # beer: Beer
    date_purchase: date
    date_untapped: date|None
    date_emptied: date|None

    class Config:
        orm_mode = True


class DrinkRecord(BaseModel):
    is_active: bool
    description: str|None = None
    amount: int
    date: date
    # purchase: Purchase

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


class PurchaseCreate(Purchase):
    beer_id: int


class DrinkRecordCreate(DrinkRecord):
    purchase_id: int


#?------------------
#? SimpleResponse
#?------------------
class HopsSimpleResponse(Hops):
    id: int


class MakerSimpleResponse(Maker):
    id: int


class BeerSimpleResponse(Beer):
    id: int
    maker: MakerSimpleResponse
    

class PurchaseSimpleResponse(Purchase):
    id: int
    # beer: BeerSimpleResponse


class DrinkRecordSimpleResponse(DrinkRecord):
    id: int
    # purchase: PurchaseSimpleResponse


#?------------------
#? Response
#?------------------
class HopsResponse(Hops):
    id: int


class MakerResponse(Maker):
    id: int
    beers: list[BeerSimpleResponse]


class BeerResponse(Beer):
    id: int
    maker: MakerSimpleResponse
    hops: list[HopsSimpleResponse]


class PurchaseResponse(Purchase):
    id: int
    beer: BeerSimpleResponse
    drink_records: list[DrinkRecordSimpleResponse]
    amount_drink: int = 0


class DrinkRecordResponse(DrinkRecord):
    id: int
    purchase: PurchaseSimpleResponse