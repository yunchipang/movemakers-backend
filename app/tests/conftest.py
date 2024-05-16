import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.settings import get_settings


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


USER1 = {
    "username": "testuser1",
    "email": "testuser1@example.com",
    "password": "password123",
}
USER2 = {
    "username": "testuser2",
    "email": "testuser2@example.com",
    "password": "password123",
}
USER3 = {
    "username": "testuser3",
    "email": "testuser3@example.com",
    "password": "password123",
}


@pytest.fixture(scope="session")
def auth_token(test_app):
    def get_token(user_data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # step 1: sign up the user
        response = test_app.post("/auth/signup/", json=user_data)
        assert response.status_code == 201

        # step 2: login to get the token
        login_payload = {
            "username": user_data["username"],
            "password": user_data["password"],
        }
        response = test_app.post("/auth/login/", data=login_payload, headers=headers)
        assert response.status_code == 200
        token = response.json()["access_token"]
        return token

    token1 = get_token(USER1)
    token2 = get_token(USER2)
    token3 = get_token(USER3)
    return {"user1": token1, "user2": token2, "user3": token3}


@pytest.fixture(scope="session")
def core_agency_id(test_app):
    payload = {
        "name": "Jam Republic",
        "website": "https://www.jamrepublicagency.com/",
        "instagram": "jamrepublictheagency",
    }
    response = test_app.post("/agencies/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample agency. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


@pytest.fixture(scope="session")
def core_contact_id(test_app, core_agency_id):
    payload = {
        "email": "info@jamrepublicagency.com",
        "agency_id": core_agency_id,
    }
    response = test_app.post("/contacts/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample contact. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


@pytest.fixture(scope="session")
def core_dancer_id(test_app, core_contact_id):
    payload = {
        "name": "Bada Lee",
        "name_orig": "이바다",
        "image_url": "https://www.jamrepublicagency.com/assets/images/image26.jpg?v=fefc6ee7",
        "pronouns": "She/Her",
        "bio": "Bada Lee, is a dancer and choreographer hailing from South Korea. Bada is a powerhouse in the Korean Entertainment scene where she has choreographed for the likes of AESPA, NCT, and The Boyz to name a few. She also dances for Lisa, CL, and Kai. We look forward to seeing more of BADA in the teaching circuit around the globe.",
        "date_of_birth": "1995-09-22",
        "nationality": "KR",
        "based_in": "Seoul",
        "instagram": "badalee__",
        "youtube": "Bada_bebe",
        "contacts": {"booking": core_contact_id},
    }
    response = test_app.post("/dancers/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample dancer. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


@pytest.fixture(scope="session")
def core_studio_id(test_app, core_dancer_id):
    sample_payload = {
        "name": "1MILLION Dance Studio",
        "address": "33, Ttukseom-ro 13-gil, Seongdong-gu, Seoul, Republic of Korea",
        "email": "team_1mstudio@1milliondance.com",
        "phone": "+82 02-512-6756",
        "opening_hours": "Monday: 4–10 PM; Tuesday: 4–10 PM; Wednesday: 4–10 PM; Thursday: 4–10 PM; Friday: 4–10 PM; Saturday: 3–9:30 PM; Sunday: 3–9:30 PM",
        "founded_in": 2013,
        "instagram": "@1milliondance",
        "youtube": "@1MILLION_Dance",
        "website": "https://www.1milliondance.com/",
        "owner_ids": [core_dancer_id],
    }
    response = test_app.post("/studios/", json=sample_payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample studio. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


@pytest.fixture(scope="session")
def core_spotify_track_id(test_app):
    payload = {
        "spotify_track_id": "6XpEm7VJ7TZxZTawH8BCSW",
        "name": "Jump",
        "artist": "Tyla",
    }
    response = test_app.post("/music/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create music. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["spotify_track_id"]
