"""
English: Seeds the UniNexus AI demo university with realistic portfolio-grade data.
        Safe to run multiple times — it skips students/courses/documents that already exist.
Roman Urdu: UniNexus AI demo university ke liye realistic portfolio-level data seed karta hai.
        Bar bar chalana safe hai — jo students/courses/documents pehle se hain, unko chhorta hai.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment
from backend.app.models.document import Document


TENANT_ID = 1

# English: 25 realistic students with mixed Pakistani + international names.
# Roman Urdu: 25 realistic students — Pakistani aur international names ka mix.
STUDENTS = [
    ('S101', 'Ali',      'Khan',     'ali.khan@demo.university.edu',      2024),
    ('S102', 'Sara',     'Ahmed',    'sara.ahmed@demo.university.edu',    2024),
    ('S103', 'Hassan',   'Raza',     'hassan.raza@demo.university.edu',   2024),
    ('S104', 'Fatima',   'Malik',    'fatima.malik@demo.university.edu',  2023),
    ('S105', 'Ayesha',   'Siddiqui', 'ayesha.s@demo.university.edu',      2024),
    ('S106', 'Ahmed',    'Al-Rashid','ahmed.rashid@demo.university.edu',  2023),
    ('S107', 'Zainab',   'Hassan',   'zainab.h@demo.university.edu',      2024),
    ('S108', 'Bilal',    'Akhtar',   'bilal.akhtar@demo.university.edu',  2022),
    ('S109', 'Maryam',   'Yousuf',   'maryam.y@demo.university.edu',      2023),
    ('S110', 'Omar',     'Farooq',   'omar.farooq@demo.university.edu',   2024),
    ('S111', 'Hira',     'Nasir',    'hira.nasir@demo.university.edu',    2024),
    ('S112', 'Usman',    'Tariq',    'usman.tariq@demo.university.edu',   2023),
    ('S113', 'Sana',     'Iqbal',    'sana.iqbal@demo.university.edu',    2024),
    ('S114', 'Kamran',   'Aslam',    'kamran.aslam@demo.university.edu',  2022),
    ('S115', 'Laiba',    'Sheikh',   'laiba.sheikh@demo.university.edu',  2023),
    ('S116', 'Faisal',   'Mehmood',  'faisal.m@demo.university.edu',      2024),
    ('S117', 'Rabia',    'Javed',    'rabia.javed@demo.university.edu',   2023),
    ('S118', 'Saad',     'Mirza',    'saad.mirza@demo.university.edu',    2024),
    ('S119', 'Nida',     'Akram',    'nida.akram@demo.university.edu',    2024),
    ('S120', 'Yasir',    'Ali',      'yasir.ali@demo.university.edu',     2023),
    ('S121', 'Anum',     'Shah',     'anum.shah@demo.university.edu',     2024),
    ('S122', 'Rehan',    'Butt',     'rehan.butt@demo.university.edu',    2022),
    ('S123', 'Mahnoor',  'Zia',      'mahnoor.zia@demo.university.edu',   2024),
    ('S124', 'Taimoor',  'Riaz',     'taimoor.riaz@demo.university.edu',  2023),
    ('S125', 'Iqra',     'Nawaz',    'iqra.nawaz@demo.university.edu',    2024),
]

# English: 10 courses across departments — matches typical undergraduate program.
# Roman Urdu: 10 courses — different departments se, typical undergraduate program ke mutabiq.
COURSES = [
    ('CS101',   'Intro to Computer Science', 3, 'Computer Science'),
    ('MATH101', 'Calculus I',                4, 'Mathematics'),
    ('PHY101',  'Physics I',                 3, 'Physics'),
    ('ENG101',  'English Composition',       3, 'English'),
    ('CS201',   'Data Structures',           4, 'Computer Science'),
    ('MATH201', 'Linear Algebra',            3, 'Mathematics'),
    ('PHY201',  'Physics II',                3, 'Physics'),
    ('STAT301', 'Probability & Statistics',  3, 'Statistics'),
    ('CS301',   'Database Systems',          4, 'Computer Science'),
    ('ENG201',  'Technical Writing',         3, 'English'),
]

# English: Attendance + grade scenarios per student.
#         Values chosen to produce variety: top performers, average, at-risk, critical.
# Roman Urdu: Har student ke liye attendance aur grade scenarios.
#         Values aise chuni hain ke variety banay: top, average, at-risk, critical.
#
# Format: (student_number, course_code, attendance_pct, grade)
ENROLLMENTS = [
    # Ali Khan — borderline (existing student, enriched)
    ('S101', 'CS101',   65.0, 'B'),
    ('S101', 'MATH101', 70.0, 'C'),
    ('S101', 'ENG101',  72.0, 'B'),

    # Sara Ahmed — high risk (existing student, enriched)
    ('S102', 'CS101',   58.0, 'A'),
    ('S102', 'MATH101', 55.0, 'B'),

    # Hassan Raza — excellent performer
    ('S103', 'CS101',   92.0, 'A'),
    ('S103', 'MATH101', 88.0, 'A'),
    ('S103', 'PHY101',  90.0, 'A'),

    # Fatima Malik — strong performer
    ('S104', 'CS101',   88.0, 'B+'),
    ('S104', 'CS201',   85.0, 'A'),
    ('S104', 'MATH201', 82.0, 'B+'),

    # Ayesha Siddiqui — average
    ('S105', 'ENG101',  78.0, 'B'),
    ('S105', 'CS101',   74.0, 'B'),
    ('S105', 'STAT301', 72.0, 'C+'),

    # Ahmed Al-Rashid — at-risk (multiple courses)
    ('S106', 'CS101',   55.0, 'D'),
    ('S106', 'MATH101', 52.0, 'D'),
    ('S106', 'PHY101',  50.0, 'F'),

    # Zainab Hassan — good performer
    ('S107', 'ENG101',  87.0, 'A'),
    ('S107', 'ENG201',  85.0, 'A'),

    # Bilal Akhtar — critical (multiple failures)
    ('S108', 'CS101',   45.0, 'F'),
    ('S108', 'MATH101', 40.0, 'F'),
    ('S108', 'CS201',   48.0, 'D'),

    # Maryam Yousuf — excellent
    ('S109', 'CS101',   95.0, 'A'),
    ('S109', 'CS201',   92.0, 'A'),
    ('S109', 'CS301',   90.0, 'A'),

    # Omar Farooq — average
    ('S110', 'MATH101', 76.0, 'B'),
    ('S110', 'PHY101',  78.0, 'B'),
    ('S110', 'STAT301', 74.0, 'B'),

    # Hira Nasir — at-risk
    ('S111', 'ENG101',  60.0, 'C'),
    ('S111', 'CS101',   58.0, 'C'),

    # Usman Tariq — good
    ('S112', 'CS101',   85.0, 'A'),
    ('S112', 'CS201',   83.0, 'B+'),
    ('S112', 'MATH201', 80.0, 'B+'),

    # Sana Iqbal — average
    ('S113', 'ENG101',  75.0, 'B'),
    ('S113', 'ENG201',  72.0, 'B'),
    ('S113', 'STAT301', 70.0, 'C+'),

    # Kamran Aslam — critical
    ('S114', 'CS201',   38.0, 'F'),
    ('S114', 'CS301',   42.0, 'D'),

    # Laiba Sheikh — good
    ('S115', 'CS101',   84.0, 'B+'),
    ('S115', 'PHY101',  82.0, 'B'),

    # Faisal Mehmood — at-risk
    ('S116', 'MATH101', 62.0, 'C'),
    ('S116', 'MATH201', 58.0, 'D'),

    # Rabia Javed — average
    ('S117', 'ENG101',  77.0, 'B'),
    ('S117', 'ENG201',  74.0, 'B'),

    # Saad Mirza — excellent
    ('S118', 'CS101',   91.0, 'A'),
    ('S118', 'CS201',   89.0, 'A'),
    ('S118', 'CS301',   88.0, 'A'),

    # Nida Akram — at-risk
    ('S119', 'CS101',   61.0, 'C'),
    ('S119', 'STAT301', 58.0, 'C'),

    # Yasir Ali — good
    ('S120', 'PHY101',  86.0, 'A'),
    ('S120', 'PHY201',  84.0, 'B+'),

    # Anum Shah — average
    ('S121', 'ENG101',  73.0, 'B'),
    ('S121', 'MATH101', 71.0, 'C+'),

    # Rehan Butt — critical
    ('S122', 'CS101',   42.0, 'F'),
    ('S122', 'MATH101', 45.0, 'D'),

    # Mahnoor Zia — excellent
    ('S123', 'CS101',   93.0, 'A'),
    ('S123', 'STAT301', 91.0, 'A'),
    ('S123', 'CS301',   90.0, 'A'),

    # Taimoor Riaz — good
    ('S124', 'CS201',   85.0, 'B+'),
    ('S124', 'CS301',   83.0, 'B+'),

    # Iqra Nawaz — average
    ('S125', 'ENG101',  74.0, 'B'),
    ('S125', 'ENG201',  72.0, 'B'),
    ('S125', 'MATH101', 70.0, 'C+'),
]


# English: 15 institutional documents with realistic content for RAG.
# Roman Urdu: 15 institutional documents — RAG ke liye realistic content.
DOCUMENTS = [
    ('Student Handbook 2026', 'Handbook',
     'Welcome to the university. This handbook covers student rights, responsibilities, academic procedures, campus facilities, code of conduct, and grievance mechanisms. All students are expected to read and comply with the policies in this document. For questions, contact the Office of Student Affairs.'),

    ('Attendance Policy 2026', 'Policy',
     'Students are required to maintain a minimum of 75% attendance in all enrolled courses. Failure to meet this threshold will result in academic intervention, including but not limited to: academic advising, mandatory tutoring, and potential course withdrawal. Extenuating circumstances must be documented and approved by the Dean.'),

    ('Examination Rules and Regulations', 'Policy',
     'Final examinations are mandatory. Students must arrive 15 minutes before the scheduled start time. Any student found with unauthorized materials will be subject to disciplinary action as per the university academic integrity policy. Re-sits are only permitted under documented medical emergencies.'),

    ('Academic Integrity Policy', 'Policy',
     'Academic honesty is fundamental to the university mission. Plagiarism, cheating, unauthorized collaboration, and falsification of records are strictly prohibited. Violations result in penalties ranging from assignment failure to expulsion. All incidents are recorded in the student academic file.'),

    ('Fee Policy 2026', 'Policy',
     'Tuition fees are payable at the start of each semester. Late payments incur a 2% monthly surcharge. Students with outstanding dues may be barred from examinations. Scholarship and financial aid recipients must maintain a minimum CGPA of 2.5 to retain benefits.'),

    ('Hostel Rules and Regulations', 'Policy',
     'Hostel residents must comply with curfew timings, visitor policies, and room maintenance standards. Smoking, alcohol, and illegal substances are strictly prohibited. Violations may lead to immediate eviction and disciplinary action. Room inspections are conducted monthly.'),

    ('Library Rules', 'Policy',
     'Students may borrow up to 5 books for 14 days. Overdue items incur a fine per day. Reference materials and periodicals are for in-library use only. Library computer access requires a valid student ID. Damaged or lost books must be replaced at market cost.'),

    ('Grading System Guidelines', 'Policy',
     'The university uses a 4.0 GPA scale. Letter grades are: A (4.0), A- (3.7), B+ (3.3), B (3.0), B- (2.7), C+ (2.3), C (2.0), D (1.0), F (0.0). A minimum CGPA of 2.0 is required for graduation. Students below 2.0 are placed on academic probation.'),

    ('Course Registration Policy', 'Policy',
     'Students register for courses during the designated registration window. Late registration requires Dean approval and incurs an administrative fee. Course changes are permitted during the first two weeks of the semester. Withdrawals after the deadline appear as W on transcripts.'),

    ('Semester System Policy', 'Policy',
     'The academic year consists of two semesters: Fall (September-December) and Spring (January-May). Each semester includes 16 weeks of instruction plus a final exam period. Summer session is optional. Credit hours per semester range from 12 to 21.'),

    ('Scholarship Guidelines', 'Policy',
     'Merit scholarships cover 25%, 50%, or 100% of tuition based on academic performance. Need-based aid requires annual documentation. Recipients must maintain a minimum CGPA of 3.0 (merit) or 2.5 (need-based). Scholarships are reviewed each semester.'),

    ('Leave of Absence Policy', 'Policy',
     'Students may request a Leave of Absence for medical, personal, or professional reasons. Approval is granted for up to two semesters. During LOA, students retain their enrollment status but cannot register for courses. Re-enrollment requires a formal request.'),

    ('Anti-Harassment Policy', 'Policy',
     'The university maintains a zero-tolerance policy toward harassment of any kind. All complaints are handled confidentially by the Office of Equity and Inclusion. Retaliation against complainants is prohibited and grounds for disciplinary action. Support services are available to all parties.'),

    ('IT Usage Policy', 'Policy',
     'University IT resources are for academic and administrative use. Users must not attempt unauthorized access, distribute malware, or violate copyright. Personal use is permitted within reasonable limits. All activity may be monitored and logged. Violations result in network access revocation.'),

    ('Campus Code of Conduct', 'Policy',
     'Students are expected to behave respectfully toward peers, faculty, and staff. Prohibited conduct includes harassment, vandalism, theft, and disruptive behavior. Violations are addressed through the student disciplinary process. Serious offenses may result in expulsion or legal action.'),

    ('Research and Thesis Guidelines', 'Policy',
     'Graduate students must complete a thesis or research project under faculty supervision. Proposals require committee approval. Ethical approval is mandatory for research involving human or animal subjects. Final submission must follow university formatting standards.'),
]


def seed():
    db = SessionLocal()
    try:
        # ---- Students ----
        added_students = 0
        for number, first, last, email, year in STUDENTS:
            exists = db.query(Student).filter(Student.student_number == number).first()
            if not exists:
                db.add(Student(
                    tenant_id=TENANT_ID, student_number=number,
                    first_name=first, last_name=last, email=email,
                    enrollment_year=year,
                ))
                added_students += 1
        db.commit()
        print(f"[Students] added {added_students}, skipped {len(STUDENTS) - added_students}")

        # ---- Courses ----
        added_courses = 0
        for code, title, hours, dept in COURSES:
            exists = db.query(Course).filter(Course.course_code == code).first()
            if not exists:
                db.add(Course(
                    tenant_id=TENANT_ID, course_code=code,
                    title=title, credit_hours=hours, department=dept,
                ))
                added_courses += 1
        db.commit()
        print(f"[Courses] added {added_courses}, skipped {len(COURSES) - added_courses}")

        # ---- Enrollments ----
        # English: Build lookup maps to avoid repeated DB queries.
        # Roman Urdu: Lookup maps bana rahe hain taake bar bar DB query na karni pare.
        student_map = {s.student_number: s.id for s in db.query(Student).all()}
        course_map = {c.course_code: c.id for c in db.query(Course).all()}

        added_enrollments = 0
        for s_num, c_code, attendance, grade in ENROLLMENTS:
            sid = student_map.get(s_num)
            cid = course_map.get(c_code)
            if not sid or not cid:
                continue
            exists = db.query(Enrollment).filter(
                Enrollment.student_id == sid,
                Enrollment.course_id == cid,
            ).first()
            if not exists:
                db.add(Enrollment(
                    student_id=sid, course_id=cid,
                    grade=grade, attendance_percentage=attendance,
                ))
                added_enrollments += 1
        db.commit()
        print(f"[Enrollments] added {added_enrollments}, skipped {len(ENROLLMENTS) - added_enrollments}")

        # ---- Documents ----
        added_documents = 0
        for title, category, content in DOCUMENTS:
            exists = db.query(Document).filter(Document.title == title).first()
            if not exists:
                db.add(Document(
                    tenant_id=TENANT_ID, title=title,
                    category=category, content=content,
                ))
                added_documents += 1
        db.commit()
        print(f"[Documents] added {added_documents}, skipped {len(DOCUMENTS) - added_documents}")

        # ---- Summary ----
        total_students = db.query(Student).count()
        total_courses = db.query(Course).count()
        total_enrollments = db.query(Enrollment).count()
        total_documents = db.query(Document).count()

        print()
        print("=" * 60)
        print("DEMO UNIVERSITY TOTALS")
        print("=" * 60)
        print(f"  Students:    {total_students}")
        print(f"  Courses:     {total_courses}")
        print(f"  Enrollments: {total_enrollments}")
        print(f"  Documents:   {total_documents}")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    seed()
