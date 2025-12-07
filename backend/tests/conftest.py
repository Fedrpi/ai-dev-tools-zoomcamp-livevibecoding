"""
Pytest fixtures for testing
"""
import asyncio
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db
from app.models import Problem, User, Session, SessionProblem, Evaluation

# Test database URL - get from environment or use default
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://livecoding:livecoding_password@localhost:5433/livecoding_test_db"
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine):
    """Create test database session"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Create test client with overridden database dependency"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_problems(db_session):
    """Get sample problems from database (seeded by migrations)"""
    from sqlalchemy import select

    # Query existing problems from database (seeded by migration)
    result = await db_session.execute(
        select(Problem).order_by(Problem.id)
    )
    problems = result.scalars().all()

    # If no problems exist (e.g., migrations not run), create them
    if not problems:
        problems = [
            Problem(
                title="Sum Two Numbers",
                difficulty="JUNIOR",
                language="PYTHON",
                description="Write a function that takes two numbers and returns their sum.",
                starter_code="def sum_two_numbers(a, b):\n    # Write your code here\n    pass",
                test_cases=[
                    {"input": [5, 3], "expected": 8},
                    {"input": [0, 0], "expected": 0},
                ]
            ),
            Problem(
                title="Find Maximum",
                difficulty="MIDDLE",
                language="PYTHON",
                description="Write a function that finds the maximum value in a list.",
                starter_code="def find_max(numbers):\n    # Write your code here\n    pass",
                test_cases=[
                    {"input": [[1, 5, 3, 9, 2]], "expected": 9},
                ]
            ),
            Problem(
                title="Binary Tree Traversal",
                difficulty="SENIOR",
                language="PYTHON",
                description="Implement in-order traversal of a binary tree.",
                starter_code="def inorder_traversal(root):\n    # Write your code here\n    pass",
                test_cases=[
                    {"input": [{"val": 1, "left": None, "right": None}], "expected": [1]},
                ]
            ),
        ]

        for problem in problems:
            db_session.add(problem)

        await db_session.commit()

        # Refresh to get IDs
        for problem in problems:
            await db_session.refresh(problem)

    return problems
