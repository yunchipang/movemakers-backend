import pytest

@pytest.fixture(scope="module")
def spotify_track_id(test_app):
    payload = {
        "spotify_track_id": "6XpEm7VJ7TZxZTawH8BCSW",
        "name": "Jump",
        "artist": "Tyla"
    }
    response = test_app.post("/music/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create music. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["spotify_track_id"]

def test_get_all_music(test_app, spotify_track_id):
    response = test_app.get("/music/")
    assert response.status_code == 200
    musics = response.json()
    assert any(
        music["spotify_track_id"] == spotify_track_id for music in musics
    ), "Music not found in the list of all music."


def test_get_music(test_app, spotify_track_id):
    response = test_app.get(f"/music/{spotify_track_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["spotify_track_id"] == spotify_track_id

def test_update_music(test_app, spotify_track_id):
    updated_payload = {
        "artist": "Tyla, Gunna, Skillibeng",
    }
    response = test_app.put(f"/music/{spotify_track_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["artist"] == "Tyla, Gunna, Skillibeng", "Music was not updated successfully."

    # fetch the music to verify the update took effect
    response = test_app.get(f"/music/{spotify_track_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["artist"] == "Tyla, Gunna, Skillibeng", "Music update did not persist."

def test_delete_music(test_app, spotify_track_id):
    # delete the music
    delete_response = test_app.delete(f"/music/{spotify_track_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted music
    fetch_response = test_app.get(f"/music/{spotify_track_id}")
    assert fetch_response.status_code == 404, "Music was not deleted successfully."