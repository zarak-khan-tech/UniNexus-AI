from backend.app.core.database import SessionLocal
from backend.app.models.document import Document

db = SessionLocal()

if db.query(Document).count() > 0:
    print("Documents already exist. Skipping seed.")
    db.close()
    exit()

doc1 = Document(
    tenant_id=1,
    title="Attendance Policy 2026",
    category="Policy",
    content="Students are required to maintain a minimum of 75% attendance in all enrolled courses. Failure to meet this threshold will result in academic intervention, including but not limited to: academic advising, mandatory tutoring, and potential course withdrawal. Extenuating circumstances must be documented and approved by the Dean."
)

doc2 = Document(
    tenant_id=1,
    title="Examination Rules and Regulations",
    category="Policy",
    content="Final examinations are mandatory. Students must arrive 15 minutes before the scheduled start time. Any student found with unauthorized materials will be subject to disciplinary action as per the university's academic integrity policy. Re-sits are only permitted under documented medical emergencies."
)

db.add_all([doc1, doc2])
db.commit()
print("Documents seeded successfully!")
db.close()
