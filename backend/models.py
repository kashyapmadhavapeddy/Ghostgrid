from sqlalchemy import Column, Integer, String, Float
from database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    current_trust_score = Column(Float, default=50.0)
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class TrustEvent(Base):
    __tablename__ = "trust_events"

    id = Column(Integer, primary_key=True, index=True)

    agent_id = Column(Integer, ForeignKey("agents.id"))

    event_type = Column(String)

    severity = Column(String)

    score_impact = Column(Float)

    agent = relationship("Agent")

class TrustSnapshot(Base):
    __tablename__ = "trust_snapshots"

    id = Column(Integer, primary_key=True)

    agent_id = Column(Integer)

    score = Column(Float)

    timestamp = Column(String)