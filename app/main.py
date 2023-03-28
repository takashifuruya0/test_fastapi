from fastapi import FastAPI
from app.routers import user, drink, base

app = FastAPI()

app.include_router(base.router)
app.include_router(user.router, prefix="/user")
app.include_router(drink.router)

