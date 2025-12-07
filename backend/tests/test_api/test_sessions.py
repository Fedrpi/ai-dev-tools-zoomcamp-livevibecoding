"""
Tests for sessions API endpoints
"""
import pytest


@pytest.mark.asyncio
async def test_create_session(client, sample_problems):
    """Test creating a new session"""
    response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    assert response.status_code == 201

    data = response.json()
    assert "session" in data
    assert "linkCode" in data

    session = data["session"]
    assert session["difficulty"] == "junior"
    assert session["language"] == "python"
    assert session["numberOfProblems"] == 1
    assert session["status"] == "waiting"
    assert session["interviewer"]["name"] == "John Doe"
    assert session["candidate"] is None
    assert len(session["problems"]) == 1


@pytest.mark.asyncio
async def test_create_session_multiple_problems(client, sample_problems):
    """Test creating session with multiple problems"""
    response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "Jane Smith",
            "difficulty": "middle",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    assert response.status_code == 201

    data = response.json()
    assert len(data["session"]["problems"]) == 1


@pytest.mark.asyncio
async def test_create_session_not_enough_problems(client, sample_problems):
    """Test creating session when not enough problems available"""
    response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "senior",
            "language": "python",
            "numberOfProblems": 3  # We only have 1 senior problem, but max is 5
        }
    )
    # Should return 400 for business logic error (not enough problems)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_session_by_id(client, sample_problems):
    """Test getting session by ID"""
    # First create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    session_id = create_response.json()["session"]["id"]

    # Now get it by ID
    response = await client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200

    data = response.json()
    assert "session" in data
    assert data["session"]["id"] == session_id


@pytest.mark.asyncio
async def test_get_session_by_id_not_found(client):
    """Test getting non-existent session"""
    response = await client.get("/api/sessions/nonexistent_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_session_by_link_code(client, sample_problems):
    """Test getting session by link code"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    link_code = create_response.json()["linkCode"]

    # Get session by link code
    response = await client.get(f"/api/sessions/by-link/{link_code}")
    assert response.status_code == 200

    data = response.json()
    assert "session" in data
    session = data["session"]
    assert "interviewer" in session
    assert session["interviewer"]["name"] == "John Doe"


@pytest.mark.asyncio
async def test_join_session(client, sample_problems):
    """Test candidate joining a session"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    session_id = create_response.json()["session"]["id"]

    # Join the session
    response = await client.post(
        f"/api/sessions/{session_id}/join",
        json={"candidateName": "Jane Smith"}
    )
    assert response.status_code == 200

    data = response.json()
    session = data["session"]
    assert session["candidate"]["name"] == "Jane Smith"
    assert session["status"] == "active"


@pytest.mark.asyncio
async def test_join_session_not_found(client):
    """Test joining non-existent session"""
    response = await client.post(
        "/api/sessions/nonexistent_id/join",
        json={"candidateName": "Jane Smith"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_end_session(client, sample_problems):
    """Test ending a session"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1
        }
    )
    session_id = create_response.json()["session"]["id"]

    # End the session
    response = await client.post(f"/api/sessions/{session_id}/end")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True

    # Verify session is ended
    get_response = await client.get(f"/api/sessions/{session_id}")
    assert get_response.json()["session"]["status"] == "ended"
    assert get_response.json()["session"]["endedAt"] is not None


@pytest.mark.asyncio
async def test_end_session_not_found(client):
    """Test ending non-existent session"""
    response = await client.post("/api/sessions/nonexistent_id/end")
    assert response.status_code == 404
