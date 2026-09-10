from fastapi import FastAPI
from backend.app.core.database import engine, Base
# IMPORT MODELS HERE so SQLAlchemy knows about them
from backend.app.models import tenant, user

app = FastAPI(
    title="UniNexus AI API",
    description="Autonomous Multi-Agent University Intelligence Platform",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to UniNexus AI API", "status": "running"}
