import pytest
from unittest.mock import patch

# ─── HELPERS ─────────────────────────────────────────────────────────────────
# Reusable setup functions to avoid repeating registration/login/session creation


def register_and_login(client, email="test@gmail.com"):
    client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": email,
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_session(client, token, topic="Python OOP"):
    response = client.post("/sessions/", json={"topic": topic},
                           headers=auth_headers(token))
    return response.json()["id"]


def create_question(client, token, session_id, difficulty="easy"):
    with patch("app.routers.sessions.generate_question",
               return_value="What is a decorator in Python?"):
        response = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": difficulty},
            headers=auth_headers(token)
        )
    return response.json()["id"]


# ─── HAPPY PATH ───────────────────────────────────────────────────────────────

def test_create_session_success(client):
    # Why: verifies the core session creation flow works end to end
    token = register_and_login(client)
    response = client.post("/sessions/", json={"topic": "Python OOP"},
                           headers=auth_headers(token))
    assert response.status_code == 201
    data = response.json()
    assert data["topic"] == "Python OOP"
    assert data["status"] == "active"
    assert "id" in data
    assert "timestamp" in data


def test_create_question_success(client):
    # Why: verifies question generation saves correctly and returns expected fields
    token = register_and_login(client)
    session_id = create_session(client, token)

    with patch("app.routers.sessions.generate_question",
               return_value="What is a decorator in Python?"):
        response = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token)
        )

    assert response.status_code == 201
    data = response.json()
    assert data["question_text"] == "What is a decorator in Python?"
    assert data["difficulty"] == "easy"
    assert data["question_number"] == 1
    assert data["session_id"] == session_id


def test_submit_answer_success(client):
    # Why: verifies the full answer submission and evaluation flow works end to end
    token = register_and_login(client)
    session_id = create_session(client, token)
    question_id = create_question(client, token, session_id)

    with patch("app.routers.sessions.evaluate_answer", return_value={
        "score": 8,
        "feedback": "Good answer, covered the main concept.",
        "model_answer": "A decorator is a function that wraps another function."
    }):
        response = client.post(
            f"/sessions/{session_id}/{question_id}/answer",
            json={"answer_text": "A decorator wraps a function to extend its behavior."},
            headers=auth_headers(token)
        )

    assert response.status_code == 201
    data = response.json()
    assert data["score"] == 8
    assert data["feedback"] == "Good answer, covered the main concept."
    assert data["model_answer"] == "A decorator is a function that wraps another function."
    assert data["answer_text"] == "A decorator wraps a function to extend its behavior."


def test_complete_session_success(client):
    # Why: verifies session status changes to completed correctly
    token = register_and_login(client)
    session_id = create_session(client, token)

    response = client.patch(f"/sessions/{session_id}/complete",
                            headers=auth_headers(token))

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


# ─── EDGE CASES ───────────────────────────────────────────────────────────────

def test_question_number_increments_correctly(client):
    # Why: verifies question_number increments properly across multiple questions
    token = register_and_login(client)
    session_id = create_session(client, token)

    with patch("app.routers.sessions.generate_question",
               return_value="Question text"):
        response1 = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token)
        )
        response2 = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token)
        )

    assert response1.json()["question_number"] == 1
    assert response2.json()["question_number"] == 2


def test_create_question_all_difficulties(client):
    # Why: verifies all three difficulty levels are accepted and saved correctly
    token = register_and_login(client)

    for difficulty in ["easy", "medium", "hard"]:
        session_id = create_session(client, token, topic=f"Topic {difficulty}")
        with patch("app.routers.sessions.generate_question",
                   return_value="A question"):
            response = client.post(
                f"/sessions/{session_id}/next-question",
                json={"difficulty": difficulty},
                headers=auth_headers(token)
            )
        assert response.status_code == 201
        assert response.json()["difficulty"] == difficulty


def test_cannot_get_question_after_session_completed(client):
    # Why: verifies active status check blocks new questions on completed sessions
    token = register_and_login(client)
    session_id = create_session(client, token)
    client.patch(f"/sessions/{session_id}/complete",
                 headers=auth_headers(token))

    with patch("app.routers.sessions.generate_question",
               return_value="A question"):
        response = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token)
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Session is no longer active"


def test_cannot_submit_answer_after_session_completed(client):
    # Why: verifies active status check blocks answer submission on completed sessions
    token = register_and_login(client)
    session_id = create_session(client, token)
    question_id = create_question(client, token, session_id)
    client.patch(f"/sessions/{session_id}/complete",
                 headers=auth_headers(token))

    with patch("app.routers.sessions.evaluate_answer", return_value={
        "score": 7, "feedback": "Good.", "model_answer": "Answer."
    }):
        response = client.post(
            f"/sessions/{session_id}/{question_id}/answer",
            json={"answer_text": "My answer"},
            headers=auth_headers(token)
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Session is no longer active"


def test_cannot_answer_same_question_twice(client):
    # Why: verifies duplicate answer protection works correctly
    token = register_and_login(client)
    session_id = create_session(client, token)
    question_id = create_question(client, token, session_id)

    with patch("app.routers.sessions.evaluate_answer", return_value={
        "score": 7, "feedback": "Good.", "model_answer": "Answer."
    }):
        client.post(
            f"/sessions/{session_id}/{question_id}/answer",
            json={"answer_text": "First answer"},
            headers=auth_headers(token)
        )
        response = client.post(
            f"/sessions/{session_id}/{question_id}/answer",
            json={"answer_text": "Second answer"},
            headers=auth_headers(token)
        )

    assert response.status_code == 400
    assert response.json()[
        "detail"] == "This question has already been answered"


# ─── ERROR CASES ──────────────────────────────────────────────────────────────

def test_create_session_nonexistent(client):
    # Why: verifies 404 is returned for sessions that don't exist
    token = register_and_login(client)
    response = client.post("/sessions/99999/next-question",
                           json={"difficulty": "easy"},
                           headers=auth_headers(token))
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_submit_answer_nonexistent_question(client):
    # Why: verifies 404 is returned for questions that don't exist
    token = register_and_login(client)
    session_id = create_session(client, token)

    response = client.post(
        f"/sessions/{session_id}/99999/answer",
        json={"answer_text": "My answer"},
        headers=auth_headers(token)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"


def test_ai_service_failure_returns_503(client):
    # Why: verifies that Anthropic API failures return 503 not an unhandled 500 crash
    token = register_and_login(client)
    session_id = create_session(client, token)

    with patch("app.routers.sessions.generate_question",
               side_effect=Exception("Anthropic API is down")):
        response = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token)
        )

    assert response.status_code == 503
    assert response.json()[
        "detail"] == "AI generation service is currently unavailable"


# ─── SECURITY ─────────────────────────────────────────────────────────────────

def test_cannot_access_another_users_session(client):
    # Why: verifies ownership check prevents user A from accessing user B's session
    token_a = register_and_login(client, email="usera@gmail.com")
    token_b = register_and_login(client, email="userb@gmail.com")

    session_id = create_session(client, token_a)

    # User B tries to create a question in User A's session
    with patch("app.routers.sessions.generate_question",
               return_value="A question"):
        response = client.post(
            f"/sessions/{session_id}/next-question",
            json={"difficulty": "easy"},
            headers=auth_headers(token_b)
        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access this session"


def test_unauthenticated_request_rejected(client):
    # Why: verifies all session endpoints require a valid JWT token
    response = client.post("/sessions/", json={"topic": "Python OOP"})
    assert response.status_code == 401


# ─── PERFORMANCE ──────────────────────────────────────────────────────────────

def test_create_5_questions_in_one_session(client):
    # Why: verifies the route handles multiple sequential questions correctly
    # and question numbers increment without gaps or duplicates
    token = register_and_login(client)
    session_id = create_session(client, token)

    question_numbers = []
    with patch("app.routers.sessions.generate_question",
               return_value="A question"):
        for _ in range(5):
            response = client.post(
                f"/sessions/{session_id}/next-question",
                json={"difficulty": "easy"},
                headers=auth_headers(token)
            )
            assert response.status_code == 201
            question_numbers.append(response.json()["question_number"])

    assert question_numbers == [1, 2, 3, 4, 5]
