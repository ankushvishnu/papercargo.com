from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Tenant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    version: str = "v1"
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentInstance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int
    template_id: int
    config: Optional[str] = None  # json string
    status: str = "stopped"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int
    input_payload: Optional[str] = None
    output_payload: Optional[str] = None
    status: str = "queued"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
