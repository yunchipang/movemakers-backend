import pytest


@pytest.fixture(scope="module")
def dancer_id(test_app):
    payload = {
        "name": "Bada Lee 이바다",
        "bio": "🌊🌊🌊 @teambebe_official",
        "date_of_birth": "1995-09-22",
        "nationality": "KR",
        "based_in": "Seoul",
        "instagram": "@badalee__",
    }
    response = test_app.post("/dancers/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create dancer. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


def test_get_all_dancers(test_app, dancer_id):
    response = test_app.get("/dancers/")
    assert response.status_code == 200
    dancers = response.json()
    assert any(
        dancer["id"] == dancer_id for dancer in dancers
    ), "Dancer not found in the list of all dancers."


def test_get_dancer(test_app, dancer_id):
    response = test_app.get(f"/dancers/{dancer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dancer_id


def test_update_dancer(test_app, dancer_id):
    updated_payload = {
        "youtube": "@badalee_",
    }
    response = test_app.put(f"/dancers/{dancer_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["youtube"] == "@badalee_", "Dancer was not updated successfully."

    # fetch the dancer to verify the update took effect
    response = test_app.get(f"/dancers/{dancer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["youtube"] == "@badalee_", "Dancer update did not persist."


def test_delete_dancer(test_app, dancer_id):
    # delete the dancer
    delete_response = test_app.delete(f"/dancers/{dancer_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted dancer
    fetch_response = test_app.get(f"/dancers/{dancer_id}")
    assert fetch_response.status_code == 404, "Dancer was not deleted successfully."
