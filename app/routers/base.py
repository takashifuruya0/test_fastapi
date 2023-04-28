from typing import Annotated
from fastapi import Path, Query, Header, routing, Depends
from models import Item
from depends import CookieAndQuery, verify_key, verify_token


router = routing.APIRouter(tags=["base"], dependencies=[Depends(verify_token), Depends(verify_key)])


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/")
async def read_query(query_or_default: CookieAndQuery):
    return {"q_or_cookie": query_or_default}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@router.get("/items/{item_id}")
def read_item(
    item_id: Annotated[int, Path(title="OK", description="item ID")], 
    q: str | None = Query(
            title="Query string!",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        )
):
    return {"item_id": item_id, "q": q}


@router.get("/header")
async def read_header(user_agent: str | None = Header(default=None, description="HELLO")):
    return {"User-Agent": user_agent}


@router.get("/verify", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items()->list:
    return [{"item": "Foo"}, {"item": "Bar"}]
