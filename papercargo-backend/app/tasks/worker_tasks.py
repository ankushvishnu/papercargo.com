from app.tasks.celery_app import celery
from app.agents.agent_core import SimpleAgent
from app.db.session import engine
from sqlmodel import Session, select
from app.db import models
import json
from datetime import datetime

@celery.task(name="app.tasks.worker_tasks.run_agent_event")
def run_agent_event(agent_instance_id: int, event: dict):
    """
    Enqueue this from API to run an agent job.
    """
    # load agent config from DB
    with Session(engine) as session:
        stmt = select(models.AgentInstance).where(models.AgentInstance.id == agent_instance_id)
        inst = session.exec(stmt).first()
        if not inst:
            return {"status":"error","error":"agent_not_found"}

        # instantiate agent (for now, simple)
        config = {}
        try:
            if inst.config:
                config = json.loads(inst.config)
        except Exception:
            config = {}

        agent = SimpleAgent(config=config)
        result = agent.handle_event(event)

        # write task record
        task = models.TaskRecord(agent_id=agent_instance_id, input_payload=json.dumps(event), output_payload=json.dumps(result), status="completed", completed_at=datetime.utcnow())
        session.add(task)
        session.commit()
        return result
