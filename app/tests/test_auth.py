sample_user = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "securepassword",
}


def test_signup_success(test_app):
    response = test_app.post("/auth/signup/", json=sample_user)
    assert response.status_code == 200
    data = response.json()
    assert data["id"]


def test_signup_email_already_exists(test_app):
    payload = {
        "email": sample_user["email"],
        "username": "anotherusername",
        "password": "anotherpassword",
    }
    response = test_app.post("/auth/signup/", json=payload)
    assert response.status_code == 400
    assert response.json().get("detail") == "Email is already in use."


def test_signup_username_already_exists(test_app):
    payload = {
        "email": "anotheremail@example.com",
        "username": sample_user["username"],
        "password": "anotherpassword",
    }
    response = test_app.post("/auth/signup/", json=payload)
    assert response.status_code == 400
    assert response.json().get("detail") == "Username is already in use."


def test_login_success(test_app):
    payload = {
        "username": sample_user["username"],
        "password": sample_user["password"],
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = test_app.post("/auth/login/", data=payload, headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(test_app):
    payload = {
        "username": sample_user["username"],
        "password": "wrongpassword",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = test_app.post("/auth/login/", data=payload, headers=headers)
    assert response.status_code == 401
    assert response.json().get("detail") == "Incorrect username or password"
