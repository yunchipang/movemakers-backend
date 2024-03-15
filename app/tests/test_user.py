sample_user = {
    "email": "testuser@example.com",
    "password": "securepassword",
}


def test_signup_success(test_app):
    response = test_app.post("/signup/", json=sample_user)
    assert response.status_code == 200
    data = response.json()
    assert data["id"]


def test_signup_email_already_exists(test_app):
    payload = {
        "email": sample_user["email"],
        "password": "anotherpassword",
    }
    response = test_app.post("/signup/", json=payload)
    assert response.status_code == 400
    assert response.json().get("detail") == "Email is already in use."


def test_login_success(test_app):
    payload = {
        "email": sample_user["email"],
        "password": sample_user["password"],
    }
    response = test_app.post("/login/", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(test_app):
    payload = {
        "email": sample_user["email"],
        "password": "wrongpassword",  # an incorrect password
    }
    response = test_app.post("/login/", json=payload)
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid user credentials."
