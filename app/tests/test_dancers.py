def test_get_all_dancers(test_app, sample_dancer_id):
    response = test_app.get("/dancers/")
    assert response.status_code == 200
    dancers = response.json()
    assert any(
        dancer["id"] == sample_dancer_id for dancer in dancers
    ), "Sample dancer not found in the list of all dancers."


def test_get_dancer(test_app, sample_dancer_id):
    response = test_app.get(f"/dancers/{sample_dancer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_dancer_id


def test_update_dancer(test_app, sample_dancer_id):
    updated_sample_payload = {
        "youtube": "@liakimhappy",
    }
    response = test_app.put(f"/dancers/{sample_dancer_id}", json=updated_sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["youtube"] == "@liakimhappy", "Dancer was not updated successfully."

    # fetch the dancer to verify the update took effect
    response = test_app.get(f"/dancers/{sample_dancer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["youtube"] == "@liakimhappy", "Dancer update did not persist."


def test_delete_dancer(test_app, sample_dancer_id):
    # delete the dancer
    delete_response = test_app.delete(f"/dancers/{sample_dancer_id}")
    assert delete_response.status_code == 200

    # attempt to fetch the deleted dancer
    fetch_response = test_app.get(f"/dancers/{sample_dancer_id}")
    assert fetch_response.status_code == 404, "Dancer was not deleted successfully."
