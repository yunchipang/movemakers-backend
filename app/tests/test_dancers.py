from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.settings import get_settings

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


# fixture for creating a dancer
# def create_dancer():
#     sample_payload = {
#         "name": "Bada Lee 이바다",
#         "bio": "🌊🌊🌊 @teambebe_official",
#         "date_of_birth": "1995-09-22",
#         "nationality": "KR",
#         "based_in": "Seoul, KR",
#         "instagram": "@badalee__",
#     }
#     response = client.post("/dancers", json=sample_payload)
#     assert response.status_code == 200
#     data = response.json()
#     yield data
#     # cleanup code to delete the dancer after tests are done
#     client.delete(f"/dancers/{data['id']}")


# def test_create_dancer(create_dancer):
#     assert create_dancer["name"] == "Bada Lee 이바다"


def test_create_dancer():
    sample_payload = {
        "name": "Bada Lee 이바다",
        "bio": "🌊🌊🌊 @teambebe_official",
        "date_of_birth": "1995-09-22",
        "nationality": "KR",
        "based_in": "Seoul, KR",
        "instagram": "@badalee__",
    }
    response = client.post("/dancers", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bada Lee 이바다"
    assert "id" in data
    dancer_id = data["id"]
    print("Bada Lee 이바다 dancer_id: ", dancer_id)


# def test_get_all_dancers():
#     response = client.get("/dancers")
#     assert response.status_code == 200
#     dancers = response.json()
#     assert isinstance(dancers, list)


# def test_get_dancer(create_dancer):
#     dancer_id = create_dancer["id"]
#     response = client.get(f"/dancers/{dancer_id}")
#     assert response.status_code == 200
#     dancer_data = response.json()
#     assert dancer_data["id"] == dancer_id
#     assert dancer_data["name"] == create_dancer["name"]


# def test_update_dancer(create_dancer):
#     dancer_id = create_dancer["id"]
#     updated_sample_payload = {
#         "name": "Bada Lee 이바다",
#         "bio": "🌊🌊🌊 @teambebe_official",
#         "date_of_birth": "1995-09-22",
#         "nationality": "KR",
#         "based_in": "Seoul, KR",
#         "instagram": "@badalee__",
#         "youtube": "@badalee__",
#     }
#     response = client.put(f"/dancers/{dancer_id}", json=updated_sample_payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["youtube"] == data["youtube"]


# def test_delete_dancer(create_dancer):
#     dancer_id = create_dancer["id"]
#     delete_response = client.delete(f"/dancers/{dancer_id}")
#     assert delete_response.status_code == 204
#     # verifying the dancer has been deleted
#     get_response = client.get(f"/dancers/{dancer_id}")
#     assert get_response.status_code == 404
