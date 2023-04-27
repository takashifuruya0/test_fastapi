from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.sql import models, database
from app.routers import user, drink, base, file, error, auth, drink_db

# create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(base.router)
app.include_router(auth.router, prefix='/auth')
app.include_router(user.router, prefix="/user")
app.include_router(drink.router)
app.include_router(file.router, prefix="/file")
app.include_router(error.router, tags=["error", ])
app.include_router(drink_db.router, prefix="/v2")


@app.exception_handler(HTTPException)
async def validation_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Oops! There is something wrong... It says '{exc.detail}'"},
    )
