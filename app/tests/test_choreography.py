import pytest


@pytest.fixture(scope="module")
def choreography_id(test_app, core_spotify_track_id, core_dancer_id):
    payload = {
        "level": "Advanced",
        "styles": ["Choreography"],
        "videos": ["https://www.youtube.com/xxxxxxxxxx"],
        "choreographer_ids": [core_dancer_id],
        "music_id": core_spotify_track_id,
    }
    response = test_app.post("/choreos/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample choreography. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


class TestChoreography:
    def test_get_all_choreos(self, test_app, choreography_id):
        response = test_app.get("/choreos/")
        assert response.status_code == 200
        choreos = response.json()
        assert any(
            choreo["id"] == choreography_id for choreo in choreos
        ), "Choreography not found in the list of all choreos."

    def test_get_choreography(self, test_app, choreography_id):
        response = test_app.get(f"/choreos/{choreography_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == choreography_id

    def test_update_choreography(self, test_app, choreography_id):
        updated_payload = {"level": "Int/Adv"}
        response = test_app.put(f"/choreos/{choreography_id}", json=updated_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["level"] == "Int/Adv", "Choreography was not updated successfully."

        response = test_app.get(f"/choreos/{choreography_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["level"] == "Int/Adv", "Choreography update did not persist."

    def test_delete_choreography(self, test_app, choreography_id):
        delete_response = test_app.delete(f"/choreos/{choreography_id}")
        assert delete_response.status_code == 200

        fetch_response = test_app.get(f"/choreos/{choreography_id}")
        assert (
            fetch_response.status_code == 404
        ), "Choreography was not deleted successfully."