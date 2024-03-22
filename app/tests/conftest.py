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


@pytest.fixture(scope="module")
def sample_dancer_id(test_app):
    sample_payload = {
        "name": "리아킴 | Lia Kim",
        "bio": "Choreographer\nCo-Founder of @1milliondance\nLeader of @1million_swf",
        "date_of_birth": "1984-05-24",
        "nationality": "KR",
        "based_in": "Seoul",
        "instagram": "@liakimhappy",
    }
    response = test_app.post("/dancers", json=sample_payload)
    data = response.json()
    return data["id"]


@pytest.fixture(scope="module")
def sample_studio_id(test_app, sample_dancer_id):
    sample_payload = {
        "name": "1MILLION Dance Studio",
        "address": "33, Ttukseom-ro 13-gil, Seongdong-gu, Seoul, Republic of Korea",
        "email": "team_1mstudio@1milliondance.com",
        "phone": "+82 02-512-6756",
        "opening_hours": "Monday: 4–10 PM; Tuesday: 4–10 PM; Wednesday: 4–10 PM; Thursday: 4–10 PM; Friday: 4–10 PM; Saturday: 3–9:30 PM; Sunday: 3–9:30 PM",
        "founded_in": 2013,
        "instagram": "1milliondance",
        "youtube": "1MILLION_Dance",
        "website": "https://www.1milliondance.com/",
        "owner_ids": [sample_dancer_id],
    }
    response = test_app.post("/studios", json=sample_payload)
    data = response.json()
    return data["id"]
