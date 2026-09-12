from fastapi import FastAPI
from backend.app.core.database import engine, Base
from backend.app.models import tenant, user, student, course, enrollment
from backend.app.api import auth, agents

app = FastAPI(
    title="UniNexus AI API",
    description="Autonomous Multi-Agent University Intelligence Platform",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(agents.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to UniNexus AI API", "status": "running"}
