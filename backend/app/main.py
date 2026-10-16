from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.database import engine, Base
from backend.app.models import tenant, user, student, course, enrollment, document, agent_execution, approval, notification, workflow
from backend.app import integrations  # noqa: F401  (triggers adapter registration)
from backend.app.api import auth, agents, stats, academic, analytics, approvals, tools, notifications, workflows, tenant as tenant_api, imports, documents, search, events as events_api, integrations

app = FastAPI(
    title='UniNexus AI API',
    description='Autonomous Multi-Agent University Intelligence Platform',
    version='0.1.0',
)

import logging

# English: Event bus demo subscriber setup.
# Roman Urdu: Event bus demo subscriber setup.
_logger = logging.getLogger("uninexus.events")


def _log_event(e):
    _logger.info(f"[event] {e.event_type} tenant={e.tenant_id} payload_keys={list(e.payload.keys())}")


from backend.app.core.events import event_bus  # noqa: E402
event_bus.subscribe("DocumentUploaded", _log_event)
event_bus.subscribe("StudentImported", _log_event)


# English: Register global error handlers for consistent API responses.
# Roman Urdu: Consistent API responses ke liye global error handlers register karo.
from backend.app.core.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers=['*'],
    expose_headers=['*'],
)

@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(agents.router)
app.include_router(stats.router)
app.include_router(academic.router)
app.include_router(analytics.router)
app.include_router(approvals.router)
app.include_router(tools.router)
app.include_router(notifications.router)
app.include_router(workflows.router)
app.include_router(tenant_api.router)
app.include_router(imports.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(events_api.router)
app.include_router(integrations.router)

@app.get('/')
def read_root():
    return {'message': 'Welcome to UniNexus AI API', 'status': 'running'}
