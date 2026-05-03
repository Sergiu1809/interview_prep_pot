from unittest.mock import patch
from tests.test_session import register_and_login, auth_headers, create_session, create_question


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def answer_question(client, token, session_id, question_id, answer_text="My answer"):
    """Submit an answer with mocked AI evaluation"""
    with patch("app.routers.sessions.evaluate_answer", return_value={
        "score": 8,
        "feedback": "Good answer.",
        "model_answer": "The ideal answer."
    }):
        response = client.post(
            f"/sessions/{session_id}/{question_id}/answer",
            json={"answer_text": answer_text},
            headers=auth_headers(token)
        )
    return response


def complete_session(client, token, session_id):
    """Mark a session as completed"""
    return client.patch(
        f"/sessions/{session_id}/complete",
        headers=auth_headers(token)
    )


# ─── GET /sessions/history/ ──────────────────────────────────────────────────

def test_get_sessions_empty(client):
    """User with no sessions should get an empty list"""
    # Why: verifies the endpoint handles zero data gracefully instead of crashing
    token = register_and_login(client)
    response = client.get("/sessions/history/", headers=auth_headers(token))

    assert response.status_code == 200
    assert response.json() == []


def test_get_sessions_returns_correct_fields(client):
    """Each session summary should have all expected fields"""
    # Why: verifies the response shape matches SessionSummary schema
    token = register_and_login(client)
    create_session(client, token, topic="Python OOP")

    response = client.get("/sessions/history/", headers=auth_headers(token))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    session = data[0]
    assert session["topic"] == "Python OOP"
    assert session["status"] == "active"
    assert "total_questions" in session
    assert "average_score" in session
    assert "timestamp" in session


def test_get_sessions_multiple(client):
    """User with multiple sessions should see all of them"""
    # Why: verifies the list grows correctly as sessions are created
    token = register_and_login(client)
    create_session(client, token, topic="Python OOP")
    create_session(client, token, topic="SQL Joins")
    create_session(client, token, topic="FastAPI")

    response = client.get("/sessions/history/", headers=auth_headers(token))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    topics = [s["topic"] for s in data]
    assert "Python OOP" in topics
    assert "SQL Joins" in topics
    assert "FastAPI" in topics


def test_get_sessions_shows_correct_total_questions(client):
    """total_questions should reflect the actual number of questions generated"""
    # Why: verifies the func.count query works correctly
    token = register_and_login(client)
    session_id = create_session(client, token)
    create_question(client, token, session_id)
    create_question(client, token, session_id)
    create_question(client, token, session_id)

    response = client.get("/sessions/history/", headers=auth_headers(token))

    data = response.json()
    assert data[0]["total_questions"] == 3


def test_get_sessions_shows_correct_average_score(client):
    """average_score should be the mean of all answered question scores"""
    # Why: verifies the func.avg query works correctly
    token = register_and_login(client)
    session_id = create_session(client, token)
    q1 = create_question(client, token, session_id)
    q2 = create_question(client, token, session_id)

    # Both answers get score 8 from the mock
    answer_question(client, token, session_id, q1)
    answer_question(client, token, session_id, q2)

    response = client.get("/sessions/history/", headers=auth_headers(token))

    data = response.json()
    assert data[0]["average_score"] == 8.0


def test_get_sessions_no_answers_shows_zero_average(client):
    """Sessions with questions but no answers should show average_score 0.0"""
    # Why: verifies the None fallback in round(average_score, 1) if average_score else 0.0
    token = register_and_login(client)
    session_id = create_session(client, token)
    create_question(client, token, session_id)

    response = client.get("/sessions/history/", headers=auth_headers(token))

    data = response.json()
    assert data[0]["average_score"] == 0.0


def test_get_sessions_shows_completed_status(client):
    """Completed sessions should show status 'completed' in history"""
    # Why: verifies history reflects the current session status
    token = register_and_login(client)
    session_id = create_session(client, token)
    complete_session(client, token, session_id)

    response = client.get("/sessions/history/", headers=auth_headers(token))

    data = response.json()
    assert data[0]["status"] == "completed"


# ─── GET /sessions/history/{session_id} ──────────────────────────────────────

def test_get_session_detail_success(client):
    """Should return full session with nested questions and answers"""
    # Why: verifies the core detail endpoint works end to end with nested data
    token = register_and_login(client)
    session_id = create_session(client, token, topic="Python OOP")
    question_id = create_question(client, token, session_id)
    answer_question(client, token, session_id, question_id)

    response = client.get(
        f"/sessions/history/{session_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Python OOP"
    assert len(data["questions"]) == 1
    assert data["questions"][0]["question_text"] == "What is a decorator in Python?"
    assert data["questions"][0]["answer"]["score"] == 8
    assert data["questions"][0]["answer"]["feedback"] == "Good answer."


def test_get_session_detail_unanswered_question(client):
    """Questions without answers should show answer as null"""
    # Why: verifies Optional[AnswerResponse] = None works correctly
    token = register_and_login(client)
    session_id = create_session(client, token)
    create_question(client, token, session_id)

    response = client.get(
        f"/sessions/history/{session_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()
    assert data["questions"][0]["answer"] is None


def test_get_session_detail_multiple_questions(client):
    """Should return all questions in correct order"""
    # Why: verifies multiple questions are all included in the response
    token = register_and_login(client)
    session_id = create_session(client, token)
    create_question(client, token, session_id)
    create_question(client, token, session_id)
    create_question(client, token, session_id)

    response = client.get(
        f"/sessions/history/{session_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()["questions"]) == 3


def test_get_session_detail_nonexistent(client):
    """Should return 404 for sessions that don't exist"""
    # Why: verifies get_session_or_raise works correctly in history context
    token = register_and_login(client)
    response = client.get(
        "/sessions/history/99999",
        headers=auth_headers(token)
    )
    assert response.status_code == 404


# ─── SECURITY ────────────────────────────────────────────────────────────────

def test_cannot_see_other_users_history(client):
    """User A should not see User B's sessions in the list"""
    # Why: verifies the user_id filter prevents cross-user data leakage
    token_a = register_and_login(client, email="usera@gmail.com")
    token_b = register_and_login(client, email="userb@gmail.com")

    create_session(client, token_a, topic="User A's session")

    response = client.get("/sessions/history/", headers=auth_headers(token_b))

    assert response.status_code == 200
    assert response.json() == []


def test_cannot_see_other_users_session_detail(client):
    """User A should not access User B's session detail"""
    # Why: verifies ownership check in get_session_or_raise blocks cross-user access
    token_a = register_and_login(client, email="usera@gmail.com")
    token_b = register_and_login(client, email="userb@gmail.com")

    session_id = create_session(client, token_a)

    response = client.get(
        f"/sessions/history/{session_id}",
        headers=auth_headers(token_b)
    )

    assert response.status_code == 403


def test_unauthenticated_history_rejected(client):
    """History endpoints should require authentication"""
    # Why: verifies JWT protection on read endpoints, not just write endpoints
    response = client.get("/sessions/history/")
    assert response.status_code == 401
