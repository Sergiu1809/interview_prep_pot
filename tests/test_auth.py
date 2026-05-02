# ─── REGISTER ────────────────────────────────────────────────────────────────

def test_register_success(client):
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "sergiu@gmail.com"
    assert data["name"] == "Sergiu"
    assert data["is_active"] == True
    assert "id" in data
    assert "hashed_password" not in data


def test_register_returns_correct_id(client):
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 201
    assert response.json()["id"] > 0


def test_register_is_active_by_default(client):
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.json()["is_active"] == True


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_missing_fields(client):
    response = client.post("/auth/register", json={
        "email": "sergiu@gmail.com"
    })
    assert response.status_code == 422


def test_register_invalid_email_format(client):
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "notanemail",
        "password": "salut123"
    })
    assert response.status_code == 422


def test_register_empty_name(client):
    response = client.post("/auth/register", json={
        "name": "",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    # Documents current behavior — add name validation if desired
    assert response.status_code == 201


def test_register_minimum_password_length(client):
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "a"
    })
    # Currently accepted — add password min length validation if desired
    assert response.status_code == 201


def test_register_very_long_name(client):
    response = client.post("/auth/register", json={
        "name": "A" * 500,
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 201


def test_register_multiple_users_get_unique_ids(client):
    response1 = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response2 = client.post("/auth/register", json={
        "name": "Alex",
        "email": "alex@gmail.com",
        "password": "salut123"
    })
    assert response1.json()["id"] != response2.json()["id"]


def test_register_email_case_sensitivity(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "SERGIU@gmail.com",
        "password": "salut123"
    })
    # Documents current behavior — change assertion if you add case-insensitive logic
    assert response.status_code == 201


def test_password_not_stored_as_plaintext(client, db_session):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    from app.models.users import User
    user = db_session.query(User).filter(
        User.email == "sergiu@gmail.com").first()
    assert user.hashed_password != "salut123"
    assert user.hashed_password.startswith("$2b$")


def test_sql_injection_in_email(client):
    response = client.post("/auth/register", json={
        "name": "Hacker",
        "email": "'; DROP TABLE users; --",
        "password": "salut123"
    })
    assert response.status_code == 422


def test_register_10_users_sequentially(client):
    for i in range(10):
        response = client.post("/auth/register", json={
            "name": f"User {i}",
            "email": f"user{i}@gmail.com",
            "password": "salut123"
        })
        assert response.status_code == 201
        assert response.json()["email"] == f"user{i}@gmail.com"


# ─── LOGIN ────────────────────────────────────────────────────────────────────

def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/login", data={
        "username": "sergiu@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_token_is_string(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/login", data={
        "username": "sergiu@gmail.com",
        "password": "salut123"
    })
    token = response.json()["access_token"]
    assert isinstance(token, str)
    assert len(token) > 0


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/login", data={
        "username": "sergiu@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "nobody@gmail.com",
        "password": "salut123"
    })
    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post("/auth/login", data={
        "username": "sergiu@gmail.com"
    })
    assert response.status_code == 422


def test_login_empty_password(client):
    client.post("/auth/register", json={
        "name": "Sergiu",
        "email": "sergiu@gmail.com",
        "password": "salut123"
    })
    response = client.post("/auth/login", data={
        "username": "sergiu@gmail.com",
        "password": ""
    })
    # OAuth2PasswordRequestForm rejects empty password as invalid form data
    assert response.status_code == 422


def test_login_wrong_email_format(client):
    response = client.post("/auth/login", data={
        "username": "notanemail",
        "password": "salut123"
    })
    assert response.status_code == 401
