# simple skill implementations — each skill is a function that returns dict
def parse_lead_from_text(text: str) -> dict:
    # naive extraction — replace with proper NER/model later
    lines = text.splitlines()
    lead = {"name": None, "email": None, "phone": None, "message": text}
    for line in lines:
        line = line.strip()
        if "@" in line and lead["email"] is None:
            lead["email"] = line
        if any(ch.isdigit() for ch in line) and lead["phone"] is None:
            # naive phone extraction
            digits = "".join([c for c in line if c.isdigit()])
            if len(digits) >= 8:
                lead["phone"] = digits
    return lead

def generate_followup(lead: dict) -> str:
    name = lead.get("name") or "there"
    return f"Hi {name}, thanks for reaching out. I saw your message: '{lead.get('message')}'. Can we schedule a quick call?"
