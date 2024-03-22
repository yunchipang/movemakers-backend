def test_get_all_studios(test_app, sample_studio_id):
    response = test_app.get("/studios")
    assert response.status_code == 200
    studios = response.json()
    assert any(
        studio["id"] == sample_studio_id for studio in studios
    ), "Sample studio not found in the list of all studios."


def test_get_studio(test_app, sample_studio_id):
    response = test_app.get(f"/studios/{sample_studio_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_studio_id


def test_update_studio(test_app, sample_studio_id):
    updated_sample_payload = {"name": "(Updated) 1MILLION Dance Studio"}
    response = test_app.put(f"/studios/{sample_studio_id}", json=updated_sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert (
        data["name"] == "(Updated) 1MILLION Dance Studio"
    ), "Studio was not updated successfully."

    # fetch the studio to verify the update took effect
    response = test_app.get(f"/studios/{sample_studio_id}")
    assert response.status_code == 200
    data = response.json()
    assert (
        data["name"] == "(Updated) 1MILLION Dance Studio"
    ), "Studio update did not persist."


def test_delete_studio(test_app, sample_studio_id):
    # delete the studio
    delete_response = test_app.delete(f"/studios/{sample_studio_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted studio
    fetch_response = test_app.get(f"/studios/{sample_studio_id}")
    assert fetch_response.status_code == 404, "Studio was not deleted successfully."
