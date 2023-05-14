from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import db_config


engine = create_engine(
    db_config.SQLALCHEMY_DATABASE_URL, 
    connect_args=db_config.CONNECT_ARGS
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()