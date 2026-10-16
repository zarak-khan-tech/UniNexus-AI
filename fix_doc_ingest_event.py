"""
English: Add DocumentUploaded event publish to document_ingest service.
Roman Urdu: document_ingest service mein DocumentUploaded event publish add karo.
"""
path = "backend/app/services/document_ingest.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if already integrated
if "event_bus.publish" in content:
    print("SKIP: event publish already present")
    raise SystemExit(0)

# 1. Add import for event_bus
old_import = "from backend.app.models.document import Document"
new_import = "from backend.app.models.document import Document\nfrom backend.app.core.events import event_bus, Event"
if old_import not in content:
    print("ERROR: Document import anchor not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

# 2. Add event publish before the final return
old_return = """    return {
        'document_id': doc_id,
        'title': title,
        'category': category or 'Policy',
        'total_chunks': len(chunks),
        'embedded_chunks': embedded,
    }"""

new_return = """    # English: Publish an event so subscribers (workflows, notifications) can react.
    # Roman Urdu: Event publish karo taake subscribers (workflows, notifications) react kar sakein.
    try:
        event_bus.publish(Event(
            event_type='DocumentUploaded',
            tenant_id=tenant_id,
            payload={
                'document_id': doc_id,
                'title': title,
                'category': category or 'Policy',
                'chunks': embedded,
            },
        ))
    except Exception as e:
        logger.warning(f"Failed to publish DocumentUploaded event: {e}")

    return {
        'document_id': doc_id,
        'title': title,
        'category': category or 'Policy',
        'total_chunks': len(chunks),
        'embedded_chunks': embedded,
    }"""

if old_return not in content:
    print("ERROR: return block anchor not found — paste document_ingest.py end lines")
    raise SystemExit(1)
content = content.replace(old_return, new_return, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: document_ingest.py now publishes DocumentUploaded event")
