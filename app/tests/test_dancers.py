import pytest


@pytest.fixture(scope="module")
def sample_dancer_id(test_app):
    sample_payload = {
        "name": "Bada Lee 이바다",
        "bio": "🌊🌊🌊 @teambebe_official",
        "date_of_birth": "1995-09-22",
        "nationality": "KR",
        "based_in": "Seoul, KR",
        "instagram": "@badalee__",
    }
    response = test_app.post("/dancers", json=sample_payload)
    data = response.json()
    return data["id"]


def test_create_and_get_dancer(test_app, sample_dancer_id):
    response = test_app.get(f"/dancers/{sample_dancer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_dancer_id
