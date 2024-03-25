import pytest


@pytest.fixture(scope="module")
def studio_id(test_app, core_dancer_id):
    payload = {
        "name": "1MILLION Dance Studio Daejeon",
        "address": "56, Dunsan-ro, Seo-gu, Daejeon, Republic of Korea",
        "email": "1mdaejeon@1milliondance.com",
        "phone": "+82 042-488-6756",
        "opening_hours": "Monday: 4–10 PM; Tuesday: 4–10 PM; Wednesday: 4–10 PM; Thursday: 4–10 PM; Friday: 4–10 PM; Saturday: 3–9:30 PM; Sunday: 3–9:30 PM",
        "instagram": "@1million_daejeon",
        "youtube": "@1MILLIONDanceStudioDJofficial",
        "website": "https://www.1milliondance.com/",
        "owner_ids": [core_dancer_id],
    }
    response = test_app.post("/studios/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample studio. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


def test_get_all_studios(test_app, studio_id):
    response = test_app.get("/studios/")
    assert response.status_code == 200
    studios = response.json()
    assert any(
        studio["id"] == studio_id for studio in studios
    ), "Studio not found in the list of all studios."


def test_get_studio(test_app, studio_id):
    response = test_app.get(f"/studios/{studio_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == studio_id


def test_update_studio(test_app, studio_id):
    updated_payload = {"name": "1MILLION Dance Studio DJ"}
    response = test_app.put(f"/studios/{studio_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert (
        data["name"] == "1MILLION Dance Studio DJ"
    ), "Studio was not updated successfully."

    # fetch the studio to verify the update took effect
    response = test_app.get(f"/studios/{studio_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "1MILLION Dance Studio DJ", "Studio update did not persist."


def test_delete_studio(test_app, studio_id):
    # delete the studio
    delete_response = test_app.delete(f"/studios/{studio_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted studio
    fetch_response = test_app.get(f"/studios/{studio_id}")
    assert fetch_response.status_code == 404, "Studio was not deleted successfully."
