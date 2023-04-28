from sqlalchemy.orm import Session
from sql import models, schemas


#?=============================
#? Maker
#?=============================
def get_maker(db: Session, maker_id: int):
    return db.query(models.MakerDB).filter(models.MakerDB.id == maker_id).first()


def get_maker_by_name(db: Session, name: str):
    return db.query(models.MakerDB).filter(models.MakerDB.name == name).first()


def list_maker(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MakerDB).offset(skip).limit(limit).all()


def create_maker(db: Session, maker: schemas.MakerCreate):
    db_maker = models.MakerDB(**maker.dict())
    db.add(db_maker)
    db.commit()
    db.refresh(db_maker)
    return db_maker


#?=============================
#? Beer
#?=============================
def get_beer(db: Session, beer_id: int):
    return db.query(models.BeerDB).filter(models.BeerDB.id == beer_id).first()


def list_beer(
    db: Session, skip: int = 0, limit: int = 100,
    name: str|None = None, maker_id: int|None = None, maker_name: str|None = None
):
    # maker
    maker_db = get_maker_by_name(db=db, name=maker_name)
    if maker_db:
        maker_id = maker_db.id
    # beer
    query = db.query(models.BeerDB)
    if name:
        query = query.filter(models.BeerDB.name == name)
    if maker_id:
        query = query.filter(models.BeerDB.maker_id == maker_id)
    return query.offset(skip).limit(limit).all()


def create_beer(db: Session, beer: schemas.BeerCreate):
    db_beer = models.BeerDB(**beer.dict())
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer
    

#?=============================
#? Hops
#?=============================
def get_hops(db: Session, hops_id: int):
    return db.query(models.HopsDB).filter(models.HopsDB.id == hops_id).first()


def get_hops_by_name(db: Session, hops_name: str):
    return db.query(models.HopsDB).filter(models.HopsDB.name == hops_name).first()


def list_hops(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.HopsDB)
    return query.offset(skip).limit(limit).all()


def create_hops(db: Session, hops: schemas.HopsCreate):
    db_hps = models.HopsDB(**hops.dict())
    db.add(db_hps)
    db.commit()
    db.refresh(db_hps)
    return db_hps
    
def relate_hops_to_beer(db: Session, hops_id: int, beer_id: int):
    db_relation = models.RelationHopsBeerDB(hops_id=hops_id, beer_id=beer_id, id=0)
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation