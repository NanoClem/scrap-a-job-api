import os
from dataclasses import dataclass, field, asdict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@dataclass
class DBConfigs:
    SQLALCHEMY_DATABASE_URL: str = os.environ.get('SQLALCHEMY_DB_URL')
    connect_args: dict = field(init=False)

    def __post_init__(self):
        self.connect_args['check_same_thread'] = (
            'sqlite' not in self.SQLALCHEMY_DATABASE_URL
        )


db_conf = DBConfigs()
engine = create_engine(**asdict(db_conf))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
