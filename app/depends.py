from typing import Annotated
from fastapi import Depends, Cookie, Header
from fastapi.exceptions import HTTPException


#?--------------------------
#? CommonParams
#?--------------------------
async def common_parameters(q:str|None=None, skip:int=0, limit:int=100):
    return {"q": q, "skip": skip, "limit": limit}


class CommonQueryParameters:
    def __init__(self, q:str|None=None, skip:int=0, limit:int=100) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit

# CommonsDep = Annotated[dict, Depends(common_parameters)]
CommonsDep = Annotated[CommonQueryParameters, Depends()]


#?--------------------------
#? Q and cookie
#?--------------------------
async def query(q:str|None=None):
    return q


async def cookie_and_query(
    q: Annotated[str, Depends(query)], 
    last_query: Annotated[str|None, Cookie]=None
    ):
    if not q:
        return last_query
    return q

# sub dependencies are not called for each request. Instead, it would use cache.
# You can set use_cache=False to make sub dependencies called for each request.
CookieAndQuery = Annotated[cookie_and_query, Depends(use_cache=False)]


#!--------------------------
#! Verify
#!--------------------------
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key