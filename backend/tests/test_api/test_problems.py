"""
Tests for problems API endpoints
"""
import pytest


@pytest.mark.asyncio
async def test_get_problems_all(client, sample_problems):
    """Test getting all problems without filters"""
    response = await client.get("/api/problems?count=3")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 3


@pytest.mark.asyncio
async def test_get_problems_by_difficulty(client, sample_problems):
    """Test filtering problems by difficulty"""
    response = await client.get("/api/problems?difficulty=junior&count=5")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 1
    assert data["problems"][0]["difficulty"] == "junior"


@pytest.mark.asyncio
async def test_get_problems_by_language(client, sample_problems):
    """Test filtering problems by language"""
    response = await client.get("/api/problems?language=python&count=5")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 3
    for problem in data["problems"]:
        assert problem["language"] == "python"


@pytest.mark.asyncio
async def test_get_problems_combined_filters(client, sample_problems):
    """Test filtering problems by difficulty and language"""
    response = await client.get("/api/problems?difficulty=middle&language=python&count=5")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 1
    assert data["problems"][0]["difficulty"] == "middle"
    assert data["problems"][0]["language"] == "python"


@pytest.mark.asyncio
async def test_get_problems_count_limit(client, sample_problems):
    """Test count parameter limits results"""
    response = await client.get("/api/problems?count=2")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) <= 2


@pytest.mark.asyncio
async def test_get_problems_schema(client, sample_problems):
    """Test that response matches expected schema"""
    response = await client.get("/api/problems?count=1")
    assert response.status_code == 200

    data = response.json()
    assert "problems" in data

    if len(data["problems"]) > 0:
        problem = data["problems"][0]
        assert "id" in problem
        assert "title" in problem
        assert "difficulty" in problem
        assert "language" in problem
        assert "description" in problem
        assert "starterCode" in problem
        assert "testCases" in problem
        assert isinstance(problem["testCases"], list)
