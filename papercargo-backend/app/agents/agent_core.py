import json
from app.agents.skills import parse_lead_from_text, generate_followup
from app.core.settings import settings

class SimpleAgent:
    """
    Very small skeleton runtime.
    - plan: decide steps
    - execute: call tools/skills
    """

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def handle_event(self, event: dict) -> dict:
        """
        event: { type: "lead_email", payload: "raw email text" }
        """
        etype = event.get("type")
        payload = event.get("payload", "")
        log = []
        output = {}

        if etype == "lead_email":
            lead = parse_lead_from_text(payload)
            log.append({"step": "parsed_lead", "result": lead})
            # simple scoring: presence of phone/email -> score
            score = 0
            if lead.get("email"): score += 50
            if lead.get("phone"): score += 30
            score += min(20, len(lead.get("message",""))//50 * 5)
            lead["score"] = score
            output["lead"] = lead
            # generate a followup message
            followup = generate_followup(lead)
            log.append({"step": "generated_followup", "result": followup})
            output["followup"] = followup

        else:
            # default echo
            output["ok"] = True
            output["echo"] = payload

        return {"status":"ok","log":log,"output":output}
