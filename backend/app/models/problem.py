"""
Problem model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum


class Difficulty(str, enum.Enum):
    """Problem difficulty enum"""
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class Language(str, enum.Enum):
    """Programming language enum"""
    PYTHON = "python"


class Problem(Base):
    """Coding problem/task model"""

    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False, index=True)
    language = Column(Enum(Language), nullable=False, index=True)
    description = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False)
    test_cases = Column(JSON, nullable=False)  # List of test cases
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Problem(id={self.id}, title='{self.title}', difficulty='{self.difficulty}')>"
