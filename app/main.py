from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from app.routers import user, drink, base, file, error

app = FastAPI()

app.include_router(base.router)
app.include_router(user.router, prefix="/user")
app.include_router(drink.router)
app.include_router(file.router, prefix="/file")
app.include_router(error.router, tags=["error", ])


@app.exception_handler(HTTPException)
async def validation_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Oops! {exc} did something. There goes a rainbow..."},
    )
