def test_get_all_trainings(test_app, sample_training_id):
    response = test_app.get("/trainings/")
    assert response.status_code == 200
    trainings = response.json()
    assert any(
        training["id"] == sample_training_id for training in trainings
    ), "Sample training not found in the list of all trainings."


# def test_get_training(test_app, sample_training_id):
#     response = test_app.get(f"/trainings/{sample_training_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == sample_training_id


# def test_update_training(test_app, sample_training_id):
#     updated_sample_payload = {"level": "Int/Adv"}
#     response = test_app.put(
#         f"/trainings/{sample_training_id}", json=updated_sample_payload
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["level"] == "Int/Adv", "Training was not updated successfully."

#     # fetch the training to verify the update took effect
#     response = test_app.get(f"/trainings/{sample_training_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["level"] == "Int/Adv", "Training update did not persist."


# def test_delete_training(test_app, sample_training_id):
#     # delete the studio
#     delete_response = test_app.delete(f"/trainings/{sample_training_id}")
#     assert delete_response.status_code == 200

#     # attempt to fetch the deleted studio
#     fetch_response = test_app.get(f"/trainings/{sample_training_id}")
#     assert fetch_response.status_code == 404, "Training was not deleted successfully."
