"""
English: One-time migration — create agent_definitions table and seed
         the 4 existing agents for tenant 1 (Demo University).
Roman Urdu: Ek dafa ka migration — agent_definitions table banao aur tenant 1
            ke 4 existing agents seed karo.
"""
import json
from backend.app.core.database import engine, SessionLocal, Base
from backend.app.models.agent_definition import AgentDefinition
from backend.app.models.tenant import Tenant

# English: Ensure table exists (create_all only adds new tables).
# Roman Urdu: Table exist kare (create_all sirf nayi tables banata hai).
Base.metadata.create_all(bind=engine)

SEED_AGENTS = [
    {
        'name': 'AttendanceAgent',
        'description': 'Finds students with low attendance via the attendance_query tool.',
        'capabilities': ['attendance_query', 'low_attendance_detection'],
        'supported_tools': ['attendance_query', 'list_students'],
    },
    {
        'name': 'PolicyAgent',
        'description': 'Returns institutional policy rules and thresholds.',
        'capabilities': ['policy_lookup', 'threshold_reporting'],
        'supported_tools': [],
    },
    {
        'name': 'RiskAgent',
        'description': 'Analyzes academic risk via the list_enrollments tool.',
        'capabilities': ['risk_analysis', 'grade_attendance_correlation'],
        'supported_tools': ['list_enrollments'],
    },
    {
        'name': 'KnowledgeAgent',
        'description': 'Retrieves university documents via semantic vector search (RAG).',
        'capabilities': ['semantic_search', 'document_retrieval'],
        'supported_tools': ['semantic_search'],
    },
]

db = SessionLocal()
try:
    tenants = db.query(Tenant).all()
    print(f"Seeding agents for {len(tenants)} tenant(s)")

    added = 0
    for t in tenants:
        for spec in SEED_AGENTS:
            exists = db.query(AgentDefinition).filter(
                AgentDefinition.tenant_id == t.id,
                AgentDefinition.name == spec['name'],
            ).first()
            if not exists:
                db.add(AgentDefinition(
                    tenant_id=t.id,
                    name=spec['name'],
                    description=spec['description'],
                    capabilities_json=json.dumps(spec['capabilities']),
                    supported_tools_json=json.dumps(spec['supported_tools']),
                    version='1.0.0',
                    is_active=True,
                    status='active',
                ))
                added += 1
    db.commit()
    total = db.query(AgentDefinition).count()
    print(f"OK: added {added} agent definitions")
    print(f"Total agent definitions: {total}")
finally:
    db.close()
