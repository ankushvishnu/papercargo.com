from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from app.db.session import get_session, create_db_and_tables
from sqlmodel import Session, select
from app.db import models
from app.tasks.worker_tasks import run_agent_event
import json

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/setup-db")
def setup_db():
    create_db_and_tables()
    return {"ok": True}

@router.post("/agents/create")
def create_agent(payload: Dict, session: Session = Depends(get_session)):
    """
    payload: {"tenant_id":1, "template_id":1, "config": {...}}
    """
    inst = models.AgentInstance(tenant_id=payload.get("tenant_id",1), template_id=payload.get("template_id",1), config=json.dumps(payload.get("config",{})))
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return {"agent_id": inst.id, "status": inst.status}

@router.post("/agents/{agent_id}/run")
def run_agent(agent_id: int, event: Dict):
    # enqueue Celery task
    task = run_agent_event.delay(agent_id, event)
    return {"task_id": task.id}
