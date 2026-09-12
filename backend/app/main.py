from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.database import engine, Base
from backend.app.models import tenant, user, student, course, enrollment, document
from backend.app.api import auth, agents

app = FastAPI(
    title="UniNexus AI API",
    description="Autonomous Multi-Agent University Intelligence Platform",
    version="0.1.0"
)

# CORS Configuration - allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(agents.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to UniNexus AI API", "status": "running"}
