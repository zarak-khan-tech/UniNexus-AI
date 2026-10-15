"""
English: One-time migration — create tool_definitions table and seed all 
registered tools for every tenant. Reads metadata from tool_registry.
Roman Urdu: Ek dafa ka migration — tool_definitions table banao aur har 
tenant ke liye registered tools seed karo.
"""
import json
from backend.app.core.database import engine, SessionLocal, Base
from backend.app.models.tool_definition import ToolDefinition
from backend.app.models.tenant import Tenant
from backend.app.tools import tool_registry

# English: Ensure the new table exists.
# Roman Urdu: Nayi table create karo.
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    tenants = db.query(Tenant).all()
    tools_meta = tool_registry.list()  # returns list of dicts with name, description, permission, input_schema
    print(f"Found {len(tools_meta)} tools to seed across {len(tenants)} tenant(s)")

    added = 0
    skipped = 0
    for t in tenants:
        for tm in tools_meta:
            exists = db.query(ToolDefinition).filter(
                ToolDefinition.tenant_id == t.id,
                ToolDefinition.name == tm['name'],
            ).first()
            if exists:
                skipped += 1
                continue
            db.add(ToolDefinition(
                tenant_id=t.id,
                name=tm['name'],
                description=tm['description'],
                permission=tm.get('permission', 'read'),
                input_schema_json=json.dumps(tm.get('input_schema') or {}),
                version='1.0.0',
                is_active=True,
            ))
            added += 1
    db.commit()
    total = db.query(ToolDefinition).count()
    print(f"OK: added {added} tool definitions, skipped {skipped}")
    print(f"Total tool definitions in DB: {total}")
finally:
    db.close()
