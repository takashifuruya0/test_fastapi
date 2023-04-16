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
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


#? Users
class BaseUser(BaseModel):
    username: str
    email: EmailStr | None = None
    disabled: bool|None = None


class UserIn(BaseUser):
    password: str 


class UserOut(BaseUser):
    pass


class UserInDB(BaseUser):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str|None = None


#? Drinks
class Maker(BaseModel):
    name: str
    state: str
    country: str = Field(example="United States")
    note: str|None


class DrinkMaster(BaseModel):
    drink_type: DrinkType
    maker: Maker
    name: str
    amount: int
    price: float

    class Config:
        schema_extra = {
            "example": {
                "drink_type": DrinkType.BEER,
                "name": "Mind Circus",
                "maker": Maker(
                    name="Russian River Brewing", 
                    state="California", 
                    country="United States"),
                "price": 35.4,
                "amount": 355,
            }
        }
    

class DrinkReview(BaseModel):
    drink_master: DrinkMaster
    user: BaseUser|None
    date: date
    comment: str
    reputation: int 


#! ----------------------------
#! Fake Data
#! ----------------------------
fake_maker_db = [
    Maker(name="Russian River Brewing", state="California", country="United States"),
    Maker(name="Knee Deep Brewing", state="California", country="United States"),
    Maker(name="一ノ蔵", state="Miyagi", country="Japan"),
    Maker(name='DAOU', state="California", country="United States", note="Famous Winery in Paso Robles, CA")
]

fake_drink_db = [
    DrinkMaster(
        drink_type=DrinkType.BEER, maker=fake_maker_db[1], 
        name="TAHOE DEEP", amount=473, price=1000),
    DrinkMaster(
        drink_type=DrinkType.BEER, maker=fake_maker_db[0], 
        name="Pliney the Elder", amount=473, price=1200),
    DrinkMaster(
        drink_type=DrinkType.SAKE, maker=fake_maker_db[2],
        name="一ノ蔵", amount=720, price=1050),
    DrinkMaster(
        drink_type=DrinkType.WINE, maker=fake_maker_db[3],
        name="Cabernet Sauvignon", amount=750, price=5600),
    DrinkMaster(
        drink_type=DrinkType.WINE, maker=fake_maker_db[3],
        name="Chardonnay", amount=750, price=4500),
    DrinkMaster(
        drink_type=DrinkType.BEER, maker=fake_maker_db[0],
        name="Faction Pale", amount=473, price=900)
]

fake_review_db = [
    DrinkReview(drink_master=fake_drink_db[1], date=date(2022,10,12), comment="Very good", reputation=5),
    DrinkReview(drink_master=fake_drink_db[0], date=date(2022,10,12), comment="Tasty and Fruity", reputation=4),
]


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        # "full_name": "John Doe",
        "email": "johndoe@example.com",
        # "hashed_password": "fakehashedsecret",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        # "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
    "tfuruya": {
        "username": "tfuruya",
        "email": "t.furuya@test.com",
        "hashed_password": "fakehashedadmin",
        "disabled": False,
    }
}