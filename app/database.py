from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import get_settings


settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    # return database.Base.metadata.create_all(bind=database.engine)
    existing_table_names = engine.table_names()
    for table in Base.metadata.tables.values():
        if table.name not in existing_table_names:
            table.create(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()