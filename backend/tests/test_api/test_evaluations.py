"""
Tests for evaluations API endpoints
"""

import pytest


@pytest.mark.asyncio
async def test_submit_evaluation(client, sample_problems):
    """Test submitting evaluation for ended session"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1,
        },
    )
    session_id = create_response.json()["session"]["id"]
    problem_id = create_response.json()["session"]["problems"][0]["id"]

    # End the session
    await client.post(f"/api/sessions/{session_id}/end")

    # Submit evaluation
    response = await client.post(
        f"/api/sessions/{session_id}/evaluate",
        json={
            "evaluations": [
                {
                    "problemId": problem_id,
                    "rating": 4,
                    "comment": "Good solution",
                    "candidateCode": "def sum_two_numbers(a, b):\n    return a + b",
                }
            ]
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert "evaluationId" in data


@pytest.mark.asyncio
async def test_submit_evaluation_multiple_problems(client, sample_problems):
    """Test submitting evaluations for multiple problems"""
    # Create a session with 2 problems
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1,
        },
    )
    session_id = create_response.json()["session"]["id"]
    problems = create_response.json()["session"]["problems"]

    # End the session
    await client.post(f"/api/sessions/{session_id}/end")

    # Submit evaluations for all problems
    evaluations = [
        {
            "problemId": p["id"],
            "rating": 4,
            "comment": f"Solution for {p['title']}",
            "candidateCode": "# code here",
        }
        for p in problems
    ]

    response = await client.post(
        f"/api/sessions/{session_id}/evaluate", json={"evaluations": evaluations}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_submit_evaluation_session_not_ended(client, sample_problems):
    """Test that evaluation fails if session is not ended"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1,
        },
    )
    session_id = create_response.json()["session"]["id"]
    problem_id = create_response.json()["session"]["problems"][0]["id"]

    # Try to submit evaluation without ending session
    response = await client.post(
        f"/api/sessions/{session_id}/evaluate",
        json={
            "evaluations": [
                {
                    "problemId": problem_id,
                    "rating": 4,
                    "comment": "Good solution",
                    "candidateCode": "# code",
                }
            ]
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_submit_evaluation_invalid_problem_id(client, sample_problems):
    """Test that evaluation fails with invalid problem ID"""
    # Create a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1,
        },
    )
    session_id = create_response.json()["session"]["id"]

    # End the session
    await client.post(f"/api/sessions/{session_id}/end")

    # Try to submit evaluation with invalid problem ID
    response = await client.post(
        f"/api/sessions/{session_id}/evaluate",
        json={
            "evaluations": [
                {
                    "problemId": 99999,  # Invalid ID
                    "rating": 4,
                    "comment": "Good solution",
                    "candidateCode": "# code",
                }
            ]
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_submit_evaluation_session_not_found(client):
    """Test submitting evaluation for non-existent session"""
    response = await client.post(
        "/api/sessions/nonexistent_id/evaluate",
        json={
            "evaluations": [
                {"problemId": 1, "rating": 4, "comment": "Good solution", "candidateCode": "# code"}
            ]
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_evaluation_rating_range(client, sample_problems):
    """Test that evaluation accepts valid rating range"""
    # Create and end a session
    create_response = await client.post(
        "/api/sessions",
        json={
            "interviewerName": "John Doe",
            "difficulty": "junior",
            "language": "python",
            "numberOfProblems": 1,
        },
    )
    session_id = create_response.json()["session"]["id"]
    problem_id = create_response.json()["session"]["problems"][0]["id"]
    await client.post(f"/api/sessions/{session_id}/end")

    # Test valid ratings (1-5)
    for rating in [1, 2, 3, 4, 5]:
        response = await client.post(
            f"/api/sessions/{session_id}/evaluate",
            json={
                "evaluations": [
                    {
                        "problemId": problem_id,
                        "rating": rating,
                        "comment": f"Rating {rating}",
                        "candidateCode": "# code",
                    }
                ]
            },
        )
        assert response.status_code == 201
