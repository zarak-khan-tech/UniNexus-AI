from backend.app.core.database import SessionLocal
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment

db = SessionLocal()

# Check if we already have data
if db.query(Student).count() > 0:
    print("Demo data already exists. Skipping seed.")
    db.close()
    exit()

# Create Students
s1 = Student(tenant_id=1, student_number="S101", first_name="Ali", last_name="Khan", email="ali@demo.edu", enrollment_year=2024)
s2 = Student(tenant_id=1, student_number="S102", first_name="Sara", last_name="Ahmed", email="sara@demo.edu", enrollment_year=2024)
db.add_all([s1, s2])
db.commit()

# Create Courses
c1 = Course(tenant_id=1, course_code="CS101", title="Intro to Computer Science", credit_hours=3, department="Computer Science")
c2 = Course(tenant_id=1, course_code="MATH101", title="Calculus I", credit_hours=4, department="Mathematics")
db.add_all([c1, c2])
db.commit()

# Create Enrollments
e1 = Enrollment(student_id=s1.id, course_id=c1.id, grade="B", attendance_percentage=65.0)
e2 = Enrollment(student_id=s2.id, course_id=c1.id, grade="A", attendance_percentage=58.0)
e3 = Enrollment(student_id=s1.id, course_id=c2.id, grade="C", attendance_percentage=70.0)
db.add_all([e1, e2, e3])
db.commit()

print("Demo data seeded successfully!")
db.close()
