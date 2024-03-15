def test_signup_success(test_app):
    sample_user = {
        "email": "test@example.com",
        "password": "securepassword",
    }
    response = test_app.post("/signup/", json=sample_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


def test_signup_email_already_exists(test_app):
    sample_user = {
        "email": "test@example.com",
        "password": "anotherpassword",
    }
    response = test_app.post("/signup/", json=sample_user)
    assert response.status_code == 400
    assert response.json().get("detail") == "Email is already in use."
