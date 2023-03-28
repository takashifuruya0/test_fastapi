from typing import Annotated
from fastapi import Path, Query, Header, routing

router = routing.APIRouter(tags=["base"])


@router.get("/")
def read_root():
    return {"Hello": "World"}


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
