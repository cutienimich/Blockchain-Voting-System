from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# ─── USERS ───────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String, nullable=False)
    email         = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role          = Column(String, default="voter")        # voter | admin
    is_verified   = Column(Boolean, default=False)         # face verified?
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    votes         = relationship("Vote", back_populates="user")

# ─── ELECTIONS ───────────────────────────────────
class Election(Base):
    __tablename__ = "elections"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time  = Column(DateTime(timezone=True), nullable=False)
    end_time    = Column(DateTime(timezone=True), nullable=False)
    is_active   = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    candidates  = relationship("Candidate", back_populates="election")
    votes       = relationship("Vote", back_populates="election")

# ─── CANDIDATES ──────────────────────────────────
class Candidate(Base):
    __tablename__ = "candidates"

    id          = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"), nullable=False)
    name        = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    election    = relationship("Election", back_populates="candidates")
    votes       = relationship("Vote", back_populates="candidate")

# ─── VOTES ───────────────────────────────────────
class Vote(Base):
    __tablename__ = "votes"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    election_id      = Column(Integer, ForeignKey("elections.id"), nullable=False)
    candidate_id     = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    transaction_hash = Column(String, nullable=True)   # blockchain tx hash
    is_flagged       = Column(Boolean, default=False)  # fraud flag
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    user             = relationship("User", back_populates="votes")
    election         = relationship("Election", back_populates="votes")
    candidate        = relationship("Candidate", back_populates="votes")