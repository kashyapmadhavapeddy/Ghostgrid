from pydantic import BaseModel

class AgentCreate(BaseModel):
    name: str
class TrustEventCreate(BaseModel):
    agent_id: int
    event_type: str
    severity: str