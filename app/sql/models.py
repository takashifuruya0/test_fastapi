from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.sql.database import Base


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

    maker = relationship("MakerDB", back_populates="beers")