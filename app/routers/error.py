from fastapi import routing
from fastapi.exceptions import RequestValidationError, HTTPException

router = routing.APIRouter()

@router.get("/error/http")
def raise_http_error():
    raise HTTPException(status_code=416, detail="Not good ...")