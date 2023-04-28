from fastapi import routing, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.database import SessionLocal, engine


router = routing.APIRouter(tags=["drink_db"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/maker/", response_model=schemas.MakerResponse)
def create_maker(maker: schemas.MakerCreate, db: Session = Depends(get_db)):
    db_maker = crud.get_maker_by_name(db, maker.name)
    if db_maker:
        raise HTTPException(status_code=400, detail=f"{maker.name} is alreadey registered")
    return crud.create_maker(db, maker)


@router.get("/maker/", response_model=list[schemas.MakerResponse])
def list_maker(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    makers = crud.get_makers(db=db, skip=skip, limit=limit)
    return makers


@router.get("/drink/beer/", response_model=list[schemas.BeerResponse])
def list_beer(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    name: str|None = None, 
    maker_id: int|None = None, maker_name: str|None = None, 
):
    makers = crud.get_beers(
        db=db, skip=skip, limit=limit, 
        name=name, maker_id=maker_id, maker_name=maker_name)
    return makers


@router.post("/drink/beer/", response_model=schemas.BeerResponse)
def create_beer(beer: schemas.BeerCreate, db: Session = Depends(get_db)):
    db_beer = crud.get_beers(db=db, name=beer.name, maker_id=beer.maker_id)
    if db_beer:
        raise HTTPException(status_code=400, detail=f"{beer.name} of {beer.maker.name} is alreadey registered")
    return crud.create_beer(db, beer=beer)