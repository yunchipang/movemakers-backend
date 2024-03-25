import pytest


@pytest.fixture(scope="module")
def training_id(test_app, core_dancer_id, core_studio_id):
    payload = {
        "level": "Beg/Int",
        "style": "Choreography",
        "start_time": "2024-03-22T19:00:00Z",
        "end_time": "2024-03-22T20:00:00Z",
        "price": 30000,
        "currency": "KRW",
        "max_slots": 60,
        "studio_id": core_studio_id,
        "instructor_ids": [core_dancer_id],
    }
    response = test_app.post("/trainings/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample training. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


def test_get_all_trainings(test_app, training_id):
    response = test_app.get("/trainings/")
    assert response.status_code == 200
    trainings = response.json()
    assert any(
        training["id"] == training_id for training in trainings
    ), "Training not found in the list of all trainings."


def test_get_training(test_app, training_id):
    response = test_app.get(f"/trainings/{training_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == training_id


def test_update_training(test_app, training_id):
    updated_payload = {"level": "Int/Adv"}
    response = test_app.put(f"/trainings/{training_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "Int/Adv", "Training was not updated successfully."

    # fetch the training to verify the update took effect
    response = test_app.get(f"/trainings/{training_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "Int/Adv", "Training update did not persist."


def test_delete_training(test_app, training_id):
    # delete the crew
    delete_response = test_app.delete(f"/trainings/{training_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted crew
    fetch_response = test_app.get(f"/trainings/{training_id}")
    assert fetch_response.status_code == 404, "Training was not deleted successfully."
