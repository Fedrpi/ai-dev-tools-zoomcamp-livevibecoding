"""
Users service - business logic for users
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def create_user(db: AsyncSession, name: str, role: str) -> User:
    """
    Create a new user
    """
    user = User(name=name, role=role)
    db.add(user)
    await db.flush()  # Flush to get the ID
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Get user by ID
    """
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
