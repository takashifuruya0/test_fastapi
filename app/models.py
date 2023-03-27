from enum import Enum
from pydantic import BaseModel, Field, EmailStr


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


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserIn(BaseUser):
    password: str 


class UserOut(BaseUser):
    pass


class UserInDB(BaseUser):
    hashed_password: str


class Maker(BaseModel):
    name: str
    state: str
    country: str = Field(example="United States")


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
    
#! ----------------------------
#! Fake Data
#! ----------------------------
fake_maker_db = [
    Maker(name="Russian River Brewing", state="California", country="United States"),
    Maker(name="Knee Deep Brewing", state="California", country="United States"),
]

fake_drink_db = [
    DrinkMaster(
        drink_type=DrinkType.BEER, maker=fake_maker_db[1], 
        name="TAHOE DEEP", amount=473, price=1000),
    DrinkMaster(
        drink_type=DrinkType.BEER, maker=fake_maker_db[0], 
        name="Pliney the Elder", amount=473, price=1200),
    # {"name": "TAHOE DEEP", "type": DrinkType.BEER},
    # {"name": "Faction Pale", "type": DrinkType.BEER},
    # {"name": "Chardonnay", "type": DrinkType.WINE},
    # {"name": "Cabernet Sauvignon", "type": DrinkType.WINE},
    # {"name": "一ノ蔵 辛口", "type": DrinkType.SAKE},
]