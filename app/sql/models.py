from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from sql.database import Base


class MakerDB(Base):
    __tablename__ = "maker"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)

    beers = relationship("BeerDB", back_populates="maker")


class BeerDB(Base):
    __tablename__ = "beer"
    
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    maker_id = Column(Integer, ForeignKey("maker.id"))
    ibu = Column(Integer, nullable=True)
    abv = Column(Float, nullable=True)
    style = Column(String, index=True, default="-")
    price_jpy = Column(Integer, index=True, nullable=True)
    price = Column(Float, index=True, nullable=True)
    currency = Column(String, index=True, nullable=True, default="JPY")

    maker = relationship("MakerDB", back_populates="beers")
    hops = relationship("HopsDB", secondary="relation_hops_beer", back_populates="beers")
    purchases = relationship("PurchaseDB", back_populates="beer")


class HopsDB(Base):
    __tablename__ = "hops"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True, nullable=True)

    beers = relationship("BeerDB", secondary="relation_hops_beer", back_populates="hops")


class RelationHopsBeerDB(Base):
    __tablename__ = "relation_hops_beer"
    id = Column(Integer, primary_key=True)
    beer_id = Column(Integer, ForeignKey("beer.id"), primary_key=True)
    hops_id = Column(Integer, ForeignKey("hops.id"), primary_key=True)



class PurchaseDB(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, index=True, nullable=True)
    beer_id = Column(Integer, ForeignKey("beer.id"))
    date_purchase = Column(Date, index=True)
    date_untapped = Column(Date, index=True, nullable=True)
    date_emptied = Column(Date, index=True, nullable=True)

    drink_records = relationship("DrinkRecordDB", back_populates="purchase")
    beer = relationship("BeerDB", back_populates="purchases")


class DrinkRecordDB(Base):
    __tablename__ = "drink_record"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, index=True, nullable=True)
    date = Column(Date, index=True)
    amount = Column(Integer, comment="Amount to drink")
    purchase_id = Column(Integer, ForeignKey("purchase.id"))

    purchase = relationship("PurchaseDB", back_populates="drink_records")