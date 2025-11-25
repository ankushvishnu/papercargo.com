from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.settings import settings

app = FastAPI(title="Papercargo Agent Engine", version="0.1.0")
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    # any startup tasks
    print("Starting Papercargo API...")

@app.get("/")
def root():
    return {"service": "papercargo-agent-engine", "env": settings.app_env}
