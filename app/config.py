from pydantic import BaseSettings

class DatabaseConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql.db"
    CONNECT_ARGS: dict = {"check_same_thread": False}

db_config = DatabaseConfig()


class Settings(BaseSettings):
    name: str = None
    debug: bool = False