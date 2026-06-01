from fastapi import FastAPI
from database import engine, SessionLocal, Base
from models import Agent, TrustEvent
from schemas import AgentCreate, TrustEventCreate
from trust_engine import calculate_score
from trust_engine import get_risk_level
from datetime import datetime
from models import Agent, TrustEvent, TrustSnapshot

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GhostGrid Running"}

@app.post("/agents/register")
def register_agent(agent: AgentCreate):

    db = SessionLocal()

    existing_agent = (
        db.query(Agent)
        .filter(Agent.name == agent.name)
        .first()
    )

    if existing_agent:
        return {
            "error": "Agent already exists"
        }

    new_agent = Agent(
        name=agent.name
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return {
        "id": new_agent.id,
        "name": new_agent.name,
        "trust_score": new_agent.current_trust_score
    }
@app.post("/events/log")
def log_event(event: TrustEventCreate):

    db = SessionLocal()

    agent = db.query(Agent).filter(
        Agent.id == event.agent_id
    ).first()

    if not agent:
        return {"error": "Agent not found"}

    new_score, impact = calculate_score(
        agent.current_trust_score,
        event.event_type
    )

    trust_event = TrustEvent(
        agent_id=event.agent_id,
        event_type=event.event_type,
        severity=event.severity,
        score_impact=impact
    )

    db.add(trust_event)

    agent.current_trust_score = new_score

    snapshot = TrustSnapshot(
    agent_id=agent.id,
    score=new_score,
    timestamp=str(datetime.utcnow())
)

    db.add(snapshot)

    db.commit() 

    return {
        "agent_id": agent.id,
        "event": event.event_type,
        "new_score": new_score
    }
@app.get("/agents/{agent_id}/trust-score")
def get_trust_score(agent_id: int):

    db = SessionLocal()

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        return {"error": "Agent not found"}

    return {
    "agent_id": agent.id,
    "name": agent.name,
    "trust_score": agent.current_trust_score,
    "risk_level": get_risk_level(
        agent.current_trust_score
    )
}
@app.get("/agents/{agent_id}/events")
def get_agent_events(agent_id: int):

    db = SessionLocal()

    events = (
        db.query(TrustEvent)
        .filter(TrustEvent.agent_id == agent_id)
        .all()
    )

    return [
        {
            "event_type": e.event_type,
            "severity": e.severity,
            "score_impact": e.score_impact
        }
        for e in events
    ]
@app.get("/agents")
def get_agents():

    db = SessionLocal()

    agents = db.query(Agent).all()

    return [
        {
            "id": a.id,
            "name": a.name,
            "trust_score": a.current_trust_score
        }
        for a in agents
    ]
@app.get("/metrics")
def metrics():

    db = SessionLocal()

    agents = db.query(Agent).all()

    total_agents = len(agents)

    avg_trust = (
        sum(a.current_trust_score for a in agents)
        / total_agents
        if total_agents > 0
        else 0
    )

    return {
        "total_agents": total_agents,
        "average_trust": round(avg_trust, 2)
    }
@app.get("/agents/{agent_id}")
def get_agent(agent_id: int):

    db = SessionLocal()

    agent = (
        db.query(Agent)
        .filter(Agent.id == agent_id)
        .first()
    )

    if not agent:
        return {"error": "Agent not found"}

    events = (
        db.query(TrustEvent)
        .filter(TrustEvent.agent_id == agent_id)
        .all()
    )

    return {
        "id": agent.id,
        "name": agent.name,
        "trust_score": agent.current_trust_score,
        "risk_level": get_risk_level(
            agent.current_trust_score
        ),
        "events": [
            {
                "event_type": e.event_type,
                "severity": e.severity,
                "score_impact": e.score_impact
            }
            for e in events
        ]
    }
@app.get("/agents/{agent_id}/timeline")
def get_timeline(agent_id: int):

    db = SessionLocal()

    snapshots = (
        db.query(TrustSnapshot)
        .filter(TrustSnapshot.agent_id == agent_id)
        .all()
    )

    return [
        {
            "score": s.score,
            "timestamp": s.timestamp
        }
        for s in snapshots
    ]
@app.get("/high-risk-agents")
def get_high_risk_agents():

    db = SessionLocal()

    agents = (
        db.query(Agent)
        .filter(Agent.current_trust_score < 50)
        .all()
    )

    return [
        {
            "id": agent.id,
            "name": agent.name,
            "trust_score": agent.current_trust_score
        }
        for agent in agents
    ]
@app.get("/agents/{agent_id}/insights")
def get_agent_insights(agent_id: int):

    db = SessionLocal()

    agent = (
        db.query(Agent)
        .filter(Agent.id == agent_id)
        .first()
    )

    if not agent:
        return {"error": "Agent not found"}

    events = (
        db.query(TrustEvent)
        .filter(TrustEvent.agent_id == agent_id)
        .all()
    )

    hallucinations = sum(
        1
        for e in events
        if e.event_type == "HALLUCINATION"
    )

    task_successes = sum(
        1
        for e in events
        if e.event_type == "TASK_SUCCESS"
    )

    recommendation = "Normal Operation"

    if agent.current_trust_score < 50:
        recommendation = (
            "Require Human Approval"
        )

    return {
        "trust_score":
            agent.current_trust_score,

        "hallucinations":
            hallucinations,

        "task_successes":
            task_successes,

        "recommendation":
            recommendation
    }
@app.get("/recent-incidents")
def get_recent_incidents():

    db = SessionLocal()

    events = (
        db.query(TrustEvent)
        .order_by(TrustEvent.id.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "agent_id": event.agent_id,
            "event_type": event.event_type,
            "severity": event.severity,
            "score_impact": event.score_impact
        }
        for event in events
    ]