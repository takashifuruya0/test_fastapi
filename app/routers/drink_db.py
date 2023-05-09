from fastapi import routing, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from depends import CommonsDep
from sql import crud, schemas
from sql.database import SessionLocal


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
def list_maker(commons: CommonsDep, db: Session = Depends(get_db)):
    maker_list = crud.list_maker(db=db, skip=commons.skip, limit=commons.limit)
    return maker_list


@router.get("/drink/beer/", response_model=list[schemas.BeerResponse])
def list_beer(
    commons: CommonsDep, db: Session = Depends(get_db),
    name: str|None = None, 
    maker_id: int|None = None, maker_name: str|None = None, 
):
    beer_list = crud.list_beer(
        db=db, skip=commons.skip, limit=commons.limit, 
        name=name, maker_id=maker_id, maker_name=maker_name)
    return beer_list


@router.post("/drink/beer/", response_model=schemas.BeerResponse)
def create_beer(beer: schemas.BeerCreate, hops: list[int], db: Session = Depends(get_db)):
    db_beer = crud.list_beer(db=db, name=beer.name, maker_id=beer.maker_id)
    if db_beer:
        raise HTTPException(status_code=400, detail=f"{beer.name} of maker_id={beer.maker_id} is alreadey registered")
    beer_db = crud.create_beer(db, beer=beer)
    if hops:
        for hops_id in hops:
            crud.relate_hops_to_beer(db=db, hops_id=hops_id, beer_id=beer_db.id)
    db.refresh(beer_db)
    return beer_db


@router.post("/hops/", response_model=schemas.HopsResponse)
def create_hops(hops: schemas.HopsCreate, db: Session = Depends(get_db)):
    db_hops = crud.get_hops_by_name(db=db, hops_name=hops.name)
    if db_hops:
        raise HTTPException(status_code=400, detail=f"{hops.name} is alreadey registered")
    return crud.create_hops(db, hops=hops)


@router.get("/hops/", response_model=list[schemas.HopsResponse])
def list_hops(commons: CommonsDep, db: Session = Depends(get_db)):
    hops_list = crud.list_hops(
        db=db, skip=commons.skip, limit=commons.limit)
    return hops_list


@router.get("/purchase/", response_model=list[schemas.PurchaseResponse])
def list_purchase(commons: CommonsDep, db: Session = Depends(get_db)):
    purchase_list = crud.list_purchase(db=db, skip=commons.skip, limit=commons.limit)
    return purchase_list


@router.post("/purchase/", response_model=schemas.PurchaseResponse)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db, purchase=purchase)


@router.get("/drink_record/", response_model=list[schemas.DrinkRecordResponse])
def list_drink_record(commons: CommonsDep, db: Session = Depends(get_db)):
    drink_record_list = crud.list_drink_record(db=db, skip=commons.skip, limit=commons.limit)
    return drink_record_list


@router.post("/drink_record/", response_model=schemas.DrinkRecordResponse)
def create_drink_record(drink_record: schemas.DrinkRecordCreate, db: Session = Depends(get_db)):
    return crud.create_drink_record(db, drink_record=drink_record)