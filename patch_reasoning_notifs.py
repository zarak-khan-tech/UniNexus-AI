path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

old = '''        db.add(approval)
        db.commit()
        db.refresh(approval)
        return approval.id
    finally:
        db.close()'''

new = '''        db.add(approval)
        db.commit()
        db.refresh(approval)

        try:
            from backend.app.services.notifications import create_notification
            create_notification(
                tenant_id=tenant_id,
                user_id=user_id,
                kind='approval',
                title='New approval request',
                body=f'{tool_name.replace("_", " ").title()} requires your review.',
                action_url='/approvals',
            )
        except Exception:
            pass

        return approval.id
    finally:
        db.close()'''

if old not in content:
    print("ERROR: pattern not found in reasoning.py")
    raise SystemExit(1)

content = content.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: reasoning.py now fires notifications on approval creation")
