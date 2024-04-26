import pytest
import uuid


@pytest.fixture(scope="module")
def training_id(test_app, core_dancer_id, core_studio_id):
    payload = {
        "level": "Beg/Int",
        "style": "Choreography",
        "start_time": "2024-03-22T19:00:00Z",
        "end_time": "2024-03-22T20:00:00Z",
        "price": 30000,
        "currency": "KRW",
        "max_slots": 2,  # only open 2 spots for test purposes
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


class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, test_app, auth_token, training_id):
        self.client = test_app
        self.training_id = training_id
        self.tokens = auth_token

    def get_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def test_register_training_successful(self):
        # register user1 and user2 for training
        response1 = self.client.post(
            f"/trainings/{self.training_id}/register",
            headers=self.get_headers(self.tokens["user1"]),
        )
        response2 = self.client.post(
            f"/trainings/{self.training_id}/register",
            headers=self.get_headers(self.tokens["user2"]),
        )
        assert response1.status_code == 201
        assert response1.json() == {
            "message": "User successfully registered for the training"
        }
        assert response2.status_code == 201
        assert response2.json() == {
            "message": "User successfully registered for the training"
        }

    def test_register_training_full(self):
        # attempt to register user 3 for the training, but no more slots
        response = self.client.post(
            f"/trainings/{self.training_id}/register",
            headers=self.get_headers(self.tokens["user3"]),
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Training is full"}

    def test_register_training_cancel(self):
        # cancel user2's registration to training (only user1 left in the training)
        response = self.client.delete(
            f"/trainings/{self.training_id}/cancel",
            headers=self.get_headers(self.tokens["user2"]),
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "User successfully unregistered from the training"
        }

    def test_register_training_already_registered(self):
        # try to register user1 again for the training, but they're already registered
        response = self.client.post(
            f"/trainings/{self.training_id}/register",
            headers=self.get_headers(self.tokens["user1"]),
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "User is already registered"}

    def test_register_training_non_existent(self):
        non_existent_training_id = str(uuid.uuid4())
        response = self.client.post(
            f"/trainings/{non_existent_training_id}/register",
            headers=self.get_headers(self.tokens["user1"]),
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Training does not exist"}


def test_delete_training(test_app, training_id):
    # delete the crew
    delete_response = test_app.delete(f"/trainings/{training_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted crew
    fetch_response = test_app.get(f"/trainings/{training_id}")
    assert fetch_response.status_code == 404, "Training was not deleted successfully."
