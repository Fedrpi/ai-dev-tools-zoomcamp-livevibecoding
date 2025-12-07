"""
Session models
"""

import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class SessionStatus(str, enum.Enum):
    """Session status enum"""

    WAITING = "waiting"
    ACTIVE = "active"
    ENDED = "ended"


class Session(Base):
    """Interview session model"""

    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    link_code = Column(String, unique=True, nullable=False, index=True)
    difficulty = Column(String, nullable=False)
    language = Column(String, nullable=False)
    number_of_problems = Column(Integer, nullable=False)
    interviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(SessionStatus), nullable=False, default=SessionStatus.WAITING)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    interviewer = relationship("User", foreign_keys=[interviewer_id])
    candidate = relationship("User", foreign_keys=[candidate_id])
    session_problems = relationship(
        "SessionProblem", back_populates="session", cascade="all, delete-orphan"
    )
    evaluations = relationship("Evaluation", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id='{self.id}', status='{self.status}', interviewer_id={self.interviewer_id})>"


class SessionProblem(Base):
    """Many-to-many relationship between sessions and problems"""

    __tablename__ = "session_problems"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    session = relationship("Session", back_populates="session_problems")
    problem = relationship("Problem")

    def __repr__(self):
        return f"<SessionProblem(session_id='{self.session_id}', problem_id={self.problem_id}, order={self.order_index})>"
