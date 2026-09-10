from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant

db = SessionLocal()
tenant = Tenant(name="Demo University", domain="demo.university.edu")
db.add(tenant)
db.commit()
db.refresh(tenant)
print(f"Created Tenant ID: {tenant.id} - {tenant.name}")
db.close()
