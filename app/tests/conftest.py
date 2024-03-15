import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.settings import get_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_app():
    settings = get_settings()
    engine = create_engine(settings.TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client  # this client can now be used in your tests

    # teardown: drop all tables after all tests are done
    Base.metadata.drop_all(bind=engine)
