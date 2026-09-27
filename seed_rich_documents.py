"""
English: Seeds 20 rich, realistic university documents for the RAG knowledge base.
        Replaces existing short documents with detailed versions.
Roman Urdu: RAG knowledge base ke liye 20 rich realistic university documents seed karta hai.
        Purane chhote documents ko detailed versions se replace karta hai.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.document import Document
from backend.app.models.tenant import Tenant


TENANT_ID = 1


# English: 20 documents — each with proper depth (250-600 words).
# Roman Urdu: 20 documents — har ek proper detail ke saath (250-600 alfaaz).
DOCUMENTS = [
    # ========== 1. STUDENT HANDBOOK ==========
    ('Student Handbook 2026', 'Handbook', '''Welcome to the university. This handbook is your primary reference for academic life, student rights, and institutional expectations.

CHAPTER 1 — ACADEMIC INTEGRITY
All students are expected to conduct themselves with the highest standards of academic honesty. Plagiarism, cheating, unauthorized collaboration, and misrepresentation of academic work are considered serious violations. Penalties range from a failing grade on the assignment to expulsion from the university. All incidents are recorded in your permanent student file.

CHAPTER 2 — ATTENDANCE AND PARTICIPATION
Regular attendance is essential for academic success. Students must maintain at least 75% attendance in every enrolled course. Attendance is monitored weekly. Students falling below the threshold will receive a formal warning from the Office of Academic Affairs. Persistent absence without documented cause may result in course withdrawal or additional disciplinary action.

CHAPTER 3 — STUDENT RIGHTS
Every student has the right to a safe learning environment, fair assessment, access to course materials, and the ability to voice concerns through the Student Grievance Committee. Discrimination based on gender, religion, ethnicity, disability, or socioeconomic background is strictly prohibited and will be met with disciplinary action.

CHAPTER 4 — GRIEVANCE PROCEDURE
Formal grievances must be submitted in writing to the Office of Student Affairs within 14 days of the incident. The Grievance Committee will investigate and respond within 21 working days. If dissatisfied with the outcome, students may appeal to the Dean of Students within 7 days of the response.

CHAPTER 5 — CAMPUS RESOURCES
Students have access to the central library, computer labs, health services, counseling center, and career guidance office. The counseling center provides free, confidential mental health support. All services are documented in the student portal.

CHAPTER 6 — COMMUNICATION
Official communication is sent to your university email address. Students are expected to check their email at least twice weekly. Missing important deadlines because you did not check your email is not a valid excuse for late submissions or missed exams.

For any questions or clarifications, please contact the Office of Student Affairs at student.affairs@university.edu or visit Room B-104 in the Admin Block.'''),

    # ========== 2. ATTENDANCE POLICY ==========
    ('Attendance Policy 2026', 'Policy', '''PURPOSE
This policy establishes clear expectations for student attendance across all undergraduate and postgraduate programs. Regular attendance is fundamental to academic success and is monitored strictly at this institution.

MINIMUM REQUIREMENT
Every enrolled student must maintain a minimum of 75% attendance in each course they are registered for. Attendance is calculated as (sessions attended) / (total sessions conducted) × 100. Labs, tutorials, and practical sessions count equally with lectures.

WEEKLY MONITORING
The Registrar Office generates weekly attendance reports. Students who fall below the 75% threshold receive an automated warning via their university email. Department heads are also notified.

CONSEQUENCES OF LOW ATTENDANCE
- 65-74%: First written warning; mandatory meeting with academic advisor.
- 50-64%: Second warning; academic probation; guardian notified.
- Below 50%: Course withdrawal by the Dean; no credit awarded; transcript reflects 'W' grade.
- Repeated violations across semesters: Academic suspension for one semester.

EXEMPTED ABSENCES
The following do not count against attendance if properly documented:
- Authorized medical leave with hospital certificate
- Representation of the university in official events (sports, debates, etc.)
- Family bereavement (up to 7 days)
- Religious obligations
- Visa or immigration appointments for international students

All exemptions require submission of supporting documents to the Office of Academic Affairs within 5 working days of return.

SPECIAL CASES
- Student athletes: department head may grant up to 20% attendance relaxation for the sport season.
- Students with documented disabilities: accommodations may include adjusted attendance requirements per disability policy.
- Pregnant students: medical documentation grants full attendance exemption for the term.

APPEALS
Students may appeal attendance decisions to the Attendance Appeals Committee within 14 days. The committee's decision is final.

This policy is reviewed annually. Questions may be directed to registrar@university.edu.'''),

    # ========== 3. EXAMINATION RULES ==========
    ('Examination Rules and Regulations', 'Policy', '''SCOPE
These rules govern all formal examinations including midterms, finals, quizzes, and practical assessments across all faculties.

ELIGIBILITY
- Minimum 75% attendance in the course
- Cleared all outstanding semester fees
- No active disciplinary sanctions
Students failing any condition are automatically barred from the exam hall.

EXAM DAY PROCEDURE
1. Arrive at least 15 minutes before the scheduled start time.
2. Bring your university ID card. No ID = no entry.
3. Mobile phones, smart watches, and unauthorized electronic devices must be deposited at the entry desk.
4. Only transparent water bottles and approved stationery allowed.
5. Latecomers arriving more than 20 minutes after start will not be admitted.

SEATING AND CONDUCT
Seating is assigned by the invigilator on the day. Silent, individual work is required. Any attempt to communicate with another student is treated as misconduct. Leaving the exam hall before the final 15 minutes requires invigilator approval.

PROHIBITED ITEMS
- Any paper or notes
- Smart devices of any kind
- Unauthorized calculators
- Headphones, earphones, earbuds
- Bags and personal belongings (must be left outside)

MISCONDUCT AND PENALTIES
Cases of cheating, impersonation, or possession of prohibited material are documented by the invigilator and reported to the Academic Integrity Committee within 24 hours. Penalties:
- First offense: F grade in the course and formal warning on the transcript.
- Second offense: Expulsion from the program for one academic year.
- Third offense: Permanent expulsion from the university.

RE-SITS AND SUPPLEMENTARY EXAMS
Re-sits are permitted only on documented medical or compassionate grounds. Applications must be submitted to the Registrar within 7 days of the missed exam. Approval is at the discretion of the Examination Board. Re-sit grades are capped at C.

RESULT DECLARATION
Results are published on the student portal within 21 days of the last exam. Grade disputes must be filed with the department chair within 10 days of result publication.

For queries: examinations@university.edu.'''),

    # ========== 4. ACADEMIC INTEGRITY ==========
    ('Academic Integrity Policy', 'Policy', '''PRINCIPLE
Academic integrity is the foundation of the university mission. Every member of our community — students, faculty, and staff — is expected to uphold the highest standards of honesty in all academic work.

DEFINITIONS
- Plagiarism: Presenting another person's ideas, words, or work as your own without proper citation.
- Cheating: Using unauthorized materials or assistance during assessments.
- Fabrication: Inventing data, sources, or research findings.
- Collusion: Unauthorized collaboration on individual assignments.
- Self-plagiarism: Submitting work from a previous course without disclosure.
- Impersonation: Taking an exam or completing work on behalf of another student.

RESPONSIBILITIES
Students are responsible for:
- Citing sources properly in all written work
- Understanding what constitutes plagiarism
- Asking instructors for clarification when unsure
- Keeping their own work secure from copying

Faculty are responsible for:
- Explaining integrity expectations at the start of each course
- Designing assessments that discourage dishonesty
- Reporting all suspected violations consistently

PENALTY LADDER
- First violation: Zero on the assessment; formal warning; integrity seminar required.
- Second violation: F in the course; transcript annotation for one year.
- Third violation: Academic suspension for one full year.
- Repeated or severe violations: Permanent expulsion and transcript notation.

INVESTIGATION PROCESS
1. Instructor documents and reports to the department chair within 5 working days.
2. Student is informed in writing and given 7 days to respond.
3. Case reviewed by the Academic Integrity Committee.
4. Decision issued within 21 days; student may appeal to the Dean of Faculty.

SUPPORT FOR STUDENTS
The university provides:
- Free citation and writing workshops through the Library
- Access to Turnitin for all coursework
- One-on-one academic writing consultations
- Confidential advice from the Ombudsman Office

All students receive training on academic integrity during orientation. New students must sign the integrity pledge before enrolling.'''),

    # ========== 5. FEE POLICY ==========
    ('Fee Policy 2026', 'Policy', '''TUITION STRUCTURE
Tuition fees are set annually by the Board of Trustees and approved by the Finance Committee. The current fee structure applies to the 2026 academic year. Fee schedules for individual programs are published on the university finance portal.

PAYMENT SCHEDULE
- Semester 1 (Fall): Due by September 15
- Semester 2 (Spring): Due by January 31
- Summer Session: Due by June 15
Students may opt for a 3-installment plan with advance approval from the Finance Office. A 2% administrative surcharge applies to installment plans.

LATE PAYMENT
Payments received after the deadline incur a 2% monthly late fee, compounded monthly. Students with outstanding dues:
- Are barred from final examinations
- Cannot register for next semester courses
- Will not receive transcripts or degree certificates

OUTSTANDING BALANCE POLICY
If a student has unpaid dues exceeding 30 days:
1. Warning email sent to student and guardian.
2. Second warning at 60 days.
3. Registration hold placed at 90 days.
4. Referral to Legal Office at 120 days.

REFUND POLICY
- Full refund (minus 5% admin fee) if withdrawal is before semester start.
- 50% refund if withdrawal occurs within first two weeks.
- No refund after week 3.

SCHOLARSHIPS AND FINANCIAL AID
Recipients of merit scholarships must maintain a minimum CGPA of 3.0. Need-based aid recipients must maintain 2.5. Both require re-verification each semester. Failure to maintain eligibility converts the scholarship to a repayable loan for that semester.

ADDITIONAL FEES
- Lab fees: PKR 5,000 per lab-based course
- Sports fee: PKR 3,000 per semester
- Library fee: PKR 1,500 per semester
- Student activity fee: PKR 2,000 per semester
- Hostel fee: PKR 45,000 per semester (optional)

REFUNDS FOR COURSE DROPS
Dropped courses within the official add/drop window receive a full refund. After that window, no refund is processed regardless of attendance.

PAYMENT METHODS
- Online bank transfer
- Credit/debit card via finance portal
- Bank draft payable to University Treasury
- Cash at Finance Office (Business hours only)

All fee-related queries: finance@university.edu or visit Room A-201.'''),

    # ========== 6. HOSTEL RULES ==========
    ('Hostel Rules and Regulations', 'Policy', '''ELIGIBILITY AND ALLOTMENT
Hostel accommodation is available to enrolled students in good standing. Priority is given to:
1. International students
2. Students residing more than 100 km from campus
3. Students with documented medical needs
Allotment is annual; renewals require a clean disciplinary record.

ROOM ALLOTMENT AND CHANGES
Rooms are assigned by the Hostel Warden. Requests for room changes must be submitted in writing and are granted only for valid reasons (medical, disciplinary safety, etc.). Unauthorized room changes result in a fine.

CURFEW AND GATE TIMINGS
- Standard curfew: 10:00 PM on weekdays, 11:00 PM on weekends
- Late entry requires prior written approval from the Warden
- Repeated late entries (3+ in a semester) lead to formal warning
- Undisclosed overnight absence from hostel may result in disciplinary action

VISITOR POLICY
- Visitors allowed in common areas only between 4:00 PM and 8:00 PM
- Guests must register at the gate
- Overnight guests are not permitted unless formally approved
- Opposite-gender visitors are not permitted in residential corridors

PROHIBITED ITEMS AND ACTIVITIES
The following are strictly prohibited in hostel premises:
- Smoking, vaping, alcohol, and any narcotics
- Cooking appliances (hot plates, rice cookers, etc.)
- Pets of any kind
- Firearms, knives, or weapons
- Loud music after 10:00 PM
- Wall mounting, drilling, or permanent alterations

HEALTH AND HYGIENE
Residents are responsible for the cleanliness of their rooms. Common areas are cleaned by staff; rooms are inspected monthly. Failure to maintain hygiene leads to:
- First offense: Warning
- Second offense: Cleaning fee
- Third offense: Room reassignment or eviction

FIRE SAFETY
Tampering with smoke detectors, fire alarms, or extinguishers is a serious violation and results in immediate eviction and possible criminal referral. Residents must evacuate during fire drills within the specified time.

MESS AND DINING
Meals are provided in the hostel dining hall per schedule. Outside food delivery is permitted at the gate only. Dining hall hours:
- Breakfast: 7:00-9:00 AM
- Lunch: 12:30-2:00 PM
- Dinner: 7:00-9:00 PM

DISCIPLINARY ACTIONS
Violations may result in:
- Warning letter
- Fine (PKR 2,000-20,000)
- Loss of hostel privileges
- Immediate eviction
- Referral to Disciplinary Committee

EVICTION
Students evicted for disciplinary reasons forfeit the semester hostel fee. Re-admission requires a personal interview with the Dean of Students.

For hostel-related queries: hostel@university.edu or contact the Warden at extension 2200.'''),

    # ========== 7. LIBRARY RULES ==========
    ('Library Rules and Usage Policy', 'Policy', '''MISSION
The university library supports teaching, learning, and research by providing access to information resources and promoting information literacy across the academic community.

MEMBERSHIP
- All enrolled students, faculty, and staff are automatically members.
- Alumni may apply for lifetime membership at a nominal fee.
- External researchers may request temporary membership through the Dean's office.

BORROWING PRIVILEGES
- Undergraduate students: Up to 3 books, 14 days
- Postgraduate students: Up to 5 books, 21 days
- Faculty: Up to 10 books, 60 days
- Staff: Up to 4 books, 30 days

RENEWALS
Books may be renewed twice, each for the original loan period, if not requested by another user. Renewals can be done online through the library portal.

FINDS FOR OVERDUE ITEMS
- PKR 20 per day per book for regular items
- PKR 100 per day per book for reserved items
- PKR 200 per day for reference materials used outside the library
Fines are capped at the replacement cost of the item.

REFERENCE MATERIALS
Encyclopedias, dictionaries, atlases, and periodicals are for in-library use only. Photocopying is available at PKR 2 per page; scanning is free.

LIBRARY COMPUTERS
Free computer access for up to 2 hours per session. Students must log in with their university ID. Printing available at PKR 5 per page (black and white), PKR 20 per page (color).

QUIET ZONES
The Reading Hall is a strict quiet zone. Group discussions are permitted only in designated Discussion Rooms, which may be booked online for up to 2 hours.

LOST OR DAMAGED ITEMS
Users are responsible for borrowed items. Lost or damaged items must be:
- Replaced with an identical copy, OR
- Paid for at current market value + 10% processing fee
Until resolved, borrowing privileges are suspended.

INFORMATION LITERACY
The library conducts workshops on:
- Academic research methods
- Citation management (Zotero, Mendeley)
- Database searching techniques
- Avoiding plagiarism
All first-year students must attend at least one workshop per semester.

LIBRARY HOURS
- Weekdays: 8:00 AM - 10:00 PM
- Saturday: 9:00 AM - 6:00 PM
- Sunday: 12:00 PM - 6:00 PM
- Exam weeks: 24/7 opening in the Central Reading Hall

ELECTRONIC RESOURCES
Access to IEEE, JSTOR, ScienceDirect, and SpringerLink is available through the university's subscription. Access requires campus network or VPN login.

For library queries: library@university.edu or extension 2300.'''),

    # ========== 8. GRADING SYSTEM ==========
    ('Grading System Guidelines', 'Policy', '''SCALE
The university uses a 4.0 grade point scale. Letter grades, grade points, and percentage equivalents:

| Letter | Grade Points | Percentage |
|--------|--------------|------------|
| A      | 4.0          | 90-100     |
| A-     | 3.7          | 85-89      |
| B+     | 3.3          | 80-84      |
| B      | 3.0          | 75-79      |
| B-     | 2.7          | 70-74      |
| C+     | 2.3          | 65-69      |
| C      | 2.0          | 60-64      |
| D      | 1.0          | 50-59      |
| F      | 0.0          | Below 50   |

CGPA CALCULATION
CGPA = Σ(Credit Hours × Grade Points) / Σ(Credit Hours)
Only courses with a grade of D or above count toward degree credit.

PASSING AND PROBATION
- Minimum passing grade: D (1.0)
- Minimum CGPA for graduation: 2.0
- CGPA between 1.5 and 2.0: Academic probation, max 12 credit hours next semester
- CGPA below 1.5 for two consecutive semesters: Academic dismissal

GRADE DISPUTES
Students who believe a grade is incorrect must:
1. Discuss with the instructor within 7 days of grade posting.
2. If unresolved, file a formal appeal with the department chair within 14 days.
3. If still unresolved, appeal to the Academic Grievance Committee within 21 days.
The Committee's decision is final.

INCOMPLETE GRADES
'Incomplete' (I) is granted only for documented medical or family emergencies. The student must complete the missing work within 4 weeks; otherwise the grade converts to F.

REPEATING COURSES
Students may repeat courses with a grade below C. Both attempts appear on the transcript; only the higher grade is used in CGPA calculation. Maximum three repeat attempts allowed.

HONOR ROLL
- Dean's List: CGPA ≥ 3.5 in a semester (min 15 credit hours)
- President's List: CGPA ≥ 3.8 in a semester (min 15 credit hours)
- Graduation Honors: Cum Laude (3.5), Magna Cum Laude (3.7), Summa Cum Laude (3.9)

TRANSCRIPT ANNOTATIONS
- W: Withdrawal without penalty
- I: Incomplete
- F: Failure
- R: Repeated course
- AU: Audit (no credit)

For grade-related inquiries: registrar@university.edu.'''),

    # ========== 9. COURSE REGISTRATION ==========
    ('Course Registration Policy', 'Policy', '''REGISTRATION WINDOWS
- Advance Registration: Two weeks before the semester ends
- Regular Registration: First week of the semester
- Late Registration: Second week of the semester (with Dean's approval + PKR 5,000 late fee)

CREDIT HOUR LIMITS
- Full-time undergraduate: 12-21 credit hours per semester
- Full-time postgraduate: 9-15 credit hours
- Overload (above limit) requires Dean's approval and a CGPA of 3.5+
- Part-time enrolment: Below 12 credit hours requires special approval

COURSE SELECTION RULES
- Prerequisites must be completed with a C or above.
- Core courses must be taken in the prescribed sequence.
- Electives require no prerequisite unless specified by the department.
- Cross-department enrollment requires permission from both department chairs.

ADD/DROP PERIOD
Students may add or drop courses during the first two weeks of the semester without penalty. Drops after week 2 appear as 'W' on the transcript. Withdrawals after week 10 are not permitted except for medical reasons.

WAITLIST PROCESS
If a course is full, students may join a waitlist. Waitlisted students are promoted automatically when a seat becomes available. Notification is sent via university email; the student has 24 hours to accept.

AUDITING A COURSE
Students may audit a course with the instructor's approval. Audited courses appear as 'AU' on the transcript, do not count for credit, and cannot be converted to graded enrollment after week 2.

REGISTRATION HOLDS
The following conditions block registration:
- Outstanding tuition balance
- Library overdue items
- Active disciplinary sanction
- Missing required documents (e.g., medical certificate)

Students with holds must resolve them at least 5 days before registration opens.

INTERNATIONAL STUDENT ADDITIONAL REQUIREMENTS
International students must:
- Maintain full-time status (12+ credit hours)
- Register before the SEVIS reporting deadline
- Confirm visa validity with the International Office

SUMMER SESSION
Optional 6-week session. Students may register for up to 9 credit hours. Same grading and attendance policies apply.

CONFIRMATION
Registration is not final until the student clicks 'Confirm Enrolment' in the student portal. Unconfirmed registrations are auto-dropped on day 8.

For registration assistance: registrar@university.edu or ext. 2100.'''),

    # ========== 10. SEMESTER SYSTEM ==========
    ('Semester System Policy', 'Policy', '''ACADEMIC CALENDAR STRUCTURE
The academic year consists of two regular semesters and one optional summer session.

FALL SEMESTER
- Duration: 16 weeks + 2 weeks exams
- Typically: September to December
- Course load: 12-21 credits
- Major intakes for new students

SPRING SEMESTER
- Duration: 16 weeks + 2 weeks exams
- Typically: February to May
- Course load: 12-21 credits
- Mid-year intake for select programs

SUMMER SESSION
- Duration: 6 weeks + 1 week exams
- Typically: June to July
- Course load: max 9 credits
- Optional; only limited courses offered

KEY DATES
- Semester start: Week 1, Monday
- Add/drop deadline: End of week 2
- Midterms: Week 8
- Fee payment deadline: End of week 1
- Final exams: Weeks 17-18

HOLIDAYS
The academic calendar includes national holidays, religious observances, and institutional breaks. Exact dates vary by year and are published on the university portal.

GRADE PUBLICATION
Final grades are published on the student portal within 21 days of the last exam.

RE-EVALUATION WINDOW
Students may request re-evaluation of an exam paper within 10 days of result declaration. Fee: PKR 2,000 per course.

WITHDRAWAL FROM SEMESTER
Complete semester withdrawal requires Dean's approval and is granted only for medical, family, or professional reasons. Refund policies apply (see Fee Policy).

ATTENDANCE AND DEFICIENCY
Students who miss more than 25% of classes without documented reason may be barred from the final exam. See Attendance Policy.

PROBATION AND DISMISSAL
Students on academic probation must meet with their advisor monthly. Failure to improve CGPA to 2.0 within two consecutive semesters leads to dismissal.

SEMESTER FREEZE
Students may freeze a semester for up to two consecutive terms with Dean's approval. Re-entry requires a formal re-enrollment application.

TRANSFER CREDITS
Transfer credits from recognized institutions are evaluated by the Registrar. Maximum 50% of degree requirements can be transferred.

For calendar-related queries: registrar@university.edu.'''),

    # ========== 11. SCHOLARSHIPS ==========
    ('Scholarship and Financial Aid Guidelines', 'Policy', '''TYPES OF SCHOLARSHIPS

1. MERIT SCHOLARSHIP
- Award: 25%, 50%, or 100% tuition waiver
- Criteria: CGPA of 3.5+ or top 5% of class
- Renewal: Maintain CGPA 3.0+ each semester
- Application: Automatic based on previous semester CGPA

2. NEED-BASED AID
- Award: Up to 100% tuition + monthly stipend
- Criteria: Documented family income below threshold
- Renewal: Annual documentation + CGPA 2.5+
- Application: Finance Office, before semester start

3. ATHLETIC SCHOLARSHIP
- Award: 50-100% tuition + sports facility access
- Criteria: State or national-level athletes
- Renewal: Maintain CGPA 2.5+ + active participation
- Application: Sports Office

4. RESEARCH FELLOWSHIP (Postgraduate)
- Award: Full tuition + monthly stipend
- Criteria: Enrolled in research-based program; publications
- Renewal: Annual progress report + supervisor recommendation

5. HARDSHIP GRANT
- Award: One-time PKR 100,000-500,000 grant
- Criteria: Documented medical, disaster, or family emergency
- Application: Anytime during the semester

6. INTERNATIONAL STUDENT SCHOLARSHIP
- Award: 25-75% tuition waiver
- Criteria: Enrolled as international student; CGPA 3.0+
- Renewal: Every semester, subject to visa validity

APPLICATION PROCESS
1. Submit online application via student portal.
2. Attach required documents (income certificate, transcripts, medical records as applicable).
3. Interview (for need-based and hardship grants).
4. Committee decision within 30 days.

MAINTAINING ELIGIBILITY
Failing to maintain minimum CGPA for a scholarship converts the award to a repayable loan for that semester. Repeated failure results in permanent revocation.

CONCURRENT AWARDS
Only one tuition-waiver scholarship may be held at a time. However, a scholarship recipient may additionally receive a hardship grant.

FRAUD AND MISREPRESENTATION
Falsifying information on a scholarship application is grounds for:
- Immediate revocation of the award
- Recovery of funds already disbursed
- Disciplinary action up to expulsion

TAX IMPLICATIONS
Depending on country, scholarship income may be taxable. Students are advised to consult the Finance Office for guidance.

For scholarship queries: scholarships@university.edu or Room A-215.'''),

    # ========== 12. LEAVE OF ABSENCE ==========
    ('Leave of Absence Policy', 'Policy', '''PURPOSE
The Leave of Absence (LOA) policy allows students to temporarily pause their academic program due to medical, personal, or professional circumstances, with the option to return without re-applying.

ELIGIBILITY
- Must be an enrolled student in good academic standing (CGPA 2.0+).
- Must have completed at least one semester.
- Must not have an active disciplinary sanction.

VALID REASONS FOR LOA
- Medical: Serious illness, surgery, mental health
- Family: Bereavement, care of sick relative
- Professional: Internship, employment, entrepreneurship
- Personal: Religious pilgrimage, visa complications, financial hardship

LOA DURATION
- Minimum: 1 semester
- Maximum: 2 consecutive semesters (1 academic year)
- Extension: Beyond 2 semesters requires a formal re-admission application

APPLICATION PROCESS
1. Obtain LOA form from Registrar's office or portal.
2. Attach supporting documents (medical certificate, employer letter, etc.).
3. Submit to Department Chair for initial review.
4. Forwarded to Dean for approval.
5. Final approval by the Registrar.

Decisions are typically issued within 14 working days.

STATUS DURING LOA
- Enrollment status: Maintained (not active)
- Fee obligation: Waived for the LOA period
- Library access: Restricted (no borrowing)
- Campus facilities: Not accessible except counseling and health center
- Student ID: Remains valid

RETURN FROM LOA
Students must notify the Registrar at least 30 days before the LOA end date. Upon return:
- Re-enrollment in the following semester
- Academic advisor assignment
- Priority registration for required courses
- If returning from medical LOA: fitness certificate required

ACADEMIC POLICY
Coursework completed before LOA is preserved. Students returning from LOA do not receive a 'gap' notation on the transcript if the LOA was approved.

FAILURE TO RETURN
If a student fails to return or notify the Registrar within 30 days after the LOA expiry, their enrollment is cancelled. Re-entry requires formal re-admission, subject to current admission criteria.

FEES
- No tuition charged during LOA.
- Any advance payment for LOA semester is refunded within 30 days.
- If LOA is requested after the fee deadline, tuition refund is subject to the standard refund policy.

For LOA queries: registrar@university.edu.'''),

    # ========== 13. ANTI-HARASSMENT ==========
    ('Anti-Harassment and Non-Discrimination Policy', 'Policy', '''COMMITMENT
The university is committed to providing a learning and working environment free from harassment, discrimination, and retaliation. Every member of our community has the right to be treated with dignity and respect.

DEFINITIONS
- Harassment: Unwelcome conduct based on protected characteristics that creates an intimidating or hostile environment.
- Discrimination: Unequal treatment based on gender, religion, ethnicity, caste, disability, sexual orientation, age, or socioeconomic background.
- Sexual Harassment: Unwelcome sexual advances, requests for favors, or other verbal/physical conduct of a sexual nature.
- Retaliation: Adverse action against an individual for reporting harassment or participating in an investigation.

PROTECTED CHARACTERISTICS
Gender, gender identity, sexual orientation, marital status, pregnancy, religion, race, ethnicity, national origin, caste, disability, age, and veteran status.

WHERE THE POLICY APPLIES
- On campus (all buildings, grounds, hostels)
- At university events (on and off campus)
- In digital spaces (email, messaging, social media, online classes)
- During internships and field placements

REPORTING MECHANISMS
- Confidential reporting: ombudsman@university.edu
- Formal complaint: Title IX / Equity Office (Room C-108)
- Emergency: Campus Security ext. 111 or police
- Anonymous tip line: (toll-free number)

Support is available regardless of whether the report is formal or informal.

INVESTIGATION PROCESS
1. Initial intake meeting within 3 working days.
2. If probable cause: formal investigation launched.
3. Investigation completed within 60 days.
4. Findings presented to the Disciplinary Committee.
5. Decision and sanctions issued within 15 days.

INTERIM MEASURES
During investigation, the university may impose:
- No-contact order
- Class schedule changes
- Temporary suspension (for severe cases)
- Counseling and support services

PENALTIES
- Warning
- Mandatory training
- Counseling
- Suspension (up to 1 year)
- Expulsion
- Referral to law enforcement (for criminal acts)

RETALIATION
Retaliation is a separate, serious violation and is investigated independently. It is grounds for immediate suspension.

SUPPORT SERVICES
- Free counseling: Center for Student Wellness
- Legal aid: referral through Dean of Students
- Academic accommodations: through department chair

CONFIDENTIALITY
The university will protect the identities of complainants and witnesses to the extent permitted by law. However, complete confidentiality cannot be guaranteed if a formal investigation is required.

For queries or support: equity@university.edu.'''),

    # ========== 14. IT USAGE ==========
    ('IT Usage and Cybersecurity Policy', 'Policy', '''SCOPE
This policy applies to all users of university IT resources including students, faculty, staff, and external contractors accessing campus networks, systems, or cloud services.

ACCEPTABLE USE
University IT resources are provided for:
- Academic research, teaching, and learning
- Administrative work
- Official university communications
- Authorized personal use (limited, reasonable)

PROHIBITED USE
Users must NOT:
- Attempt unauthorized access to systems, networks, or data
- Share login credentials with anyone
- Install unauthorized software or pirated content
- Use university resources for commercial activity
- Distribute malware, phishing, or spam
- Violate copyright or intellectual property laws
- Access, store, or transmit illegal content
- Bypass security controls (firewalls, VPN policies)

PASSWORDS AND AUTHENTICATION
- Passwords must be at least 12 characters, mixed case, with a number and symbol.
- Passwords must be changed every 180 days.
- Multi-factor authentication (MFA) is mandatory for all staff and encouraged for students.
- Reusing your university password on other services is prohibited.

DATA CLASSIFICATION
- Public: Can be shared freely.
- Internal: Limited to university members.
- Confidential: Restricted to authorized individuals (grades, personal records).
- Restricted: Highest protection (medical, financial, research IP).

DATA HANDLING
- Confidential and restricted data must be stored only on approved systems.
- External cloud storage (Google Drive personal, Dropbox) is NOT permitted for confidential data.
- USB drives must be encrypted for university use.

EMAIL AND COMMUNICATION
- University email is the official channel for academic and administrative communication.
- Phishing awareness is mandatory; suspicious emails should be reported to itsecurity@university.edu.
- Email forwarding to external accounts must be approved.

NETWORK ACCESS
- Campus Wi-Fi requires authentication via student/faculty ID.
- VPN is required for off-campus access to internal resources.
- Guest Wi-Fi is limited and monitored.

MONITORING AND PRIVACY
The university may monitor network traffic, system access, and email for security, legal, or investigative purposes. Users should have no expectation of privacy on university systems.

INCIDENT REPORTING
Any suspected security incident (unauthorized access, lost device, data breach) must be reported within 24 hours to itsecurity@university.edu.

PENALTIES
Violations may result in:
- Warning
- Loss of IT privileges
- Disciplinary action
- Criminal referral (for serious violations)

For IT queries: ithelp@university.edu or ext. 2500.'''),

    # ========== 15. CAMPUS CODE OF CONDUCT ==========
    ('Campus Code of Conduct', 'Policy', '''PURPOSE
This code establishes behavioral expectations for all students and forms the foundation of a respectful, safe, and productive campus community.

CORE VALUES
- Respect for others
- Integrity in all actions
- Responsibility for one's conduct
- Accountability for the community

EXPECTED BEHAVIOR
- Treat peers, faculty, and staff with courtesy.
- Attend classes on time and prepared.
- Comply with all university policies.
- Maintain academic honesty.
- Respect campus property and environment.
- Report violations you witness.

PROHIBITED CONDUCT
- Disruption of classes, exams, or university events
- Verbal abuse, threats, or intimidation
- Physical violence or fighting
- Vandalism or destruction of property
- Theft or unauthorized possession of university property
- Forgery, falsification, or misuse of university documents
- Possession or use of alcohol, narcotics, or illegal substances on campus
- Possession of weapons on campus
- Unauthorized use of university trademarks or logos
- Bullying, hazing, or cyberbullying
- Doxxing or unauthorized sharing of personal information

DISCIPLINARY PROCESS
1. Incident reported to the Office of Student Affairs.
2. Student notified in writing within 5 working days.
3. Preliminary investigation by the Disciplinary Committee.
4. Student has 7 days to respond.
5. Hearing (if requested).
6. Decision issued within 21 days of complaint.

PENALTIES
- Verbal warning
- Written warning
- Community service
- Loss of privileges (campus access, hostel, etc.)
- Fine (PKR 5,000 - 50,000)
- Suspension (up to 2 semesters)
- Expulsion
- Referral to law enforcement

APPEALS
Students may appeal disciplinary decisions to the Dean of Students within 14 days. Appeals must be in writing with supporting evidence. The Dean's decision is final.

RESTORATIVE JUSTICE
For minor violations, the university may offer a restorative-justice track: mediation, acknowledgment of harm, and community restoration instead of formal penalties.

RECORDS
Disciplinary records are maintained by Student Affairs. Minor infractions are removed after graduation; serious violations remain on the permanent record.

SPECIAL CASES
Behavior related to a documented disability is handled with accommodation. Students with active mental health crises are referred to the Counseling Center before disciplinary action.

For conduct-related queries: student.affairs@university.edu.'''),

    # ========== 16. RESEARCH AND THESIS ==========
    ('Research and Thesis Guidelines', 'Policy', '''SCOPE
These guidelines apply to all research-based programs including MS, MPhil, and PhD. They govern proposal, supervision, ethics, and final submission.

SUPERVISOR ALLOCATION
- Assigned by the Department Research Committee in the first semester.
- Student may request a change with valid reason (subject to committee approval).
- Each supervisor typically guides 3-5 students concurrently.

PROPOSAL REQUIREMENTS
The research proposal must include:
- Problem statement
- Literature review (minimum 20 references)
- Research objectives and questions
- Methodology
- Expected outcomes
- Timeline (12-36 months depending on program)

The proposal must be defended before the Departmental Research Committee. Approval is required before any data collection begins.

ETHICAL APPROVAL
Research involving humans, animals, or sensitive data requires Ethics Committee approval. Applications must include:
- Detailed protocol
- Informed consent form
- Risk assessment
- Data protection plan
Approval typically takes 4-6 weeks. No data collection may begin without it.

PROGRESS MONITORING
- Monthly supervision meetings (documented)
- Semester progress reports signed by supervisor
- Annual review by the Departmental Research Committee
Unsatisfactory progress may lead to probation or termination.

THESIS FORMAT
- Front matter: title page, dedication, acknowledgments, abstract, table of contents
- Chapters: Introduction, Literature Review, Methodology, Results, Discussion, Conclusion
- References: APA 7th edition (or program-specific style)
- Font: Times New Roman 12pt
- Line spacing: 1.5
- Margins: 1.25 inches left, 1 inch other sides

PLAGIARISM CHECK
Thesis must pass a Turnitin check with similarity below 15%. Higher similarity requires supervisor explanation and committee approval.

DEFENSE
- Pre-defense: internal committee review
- Final defense: open to faculty and peers
- Defense panel: 3-5 members including one external examiner
- Passing: unanimous approval (or majority with revisions)

REVISIONS AND SUBMISSION
After defense, students have up to 90 days to submit final version with corrections. Final submission includes:
- Signed approval page
- PDF copy for digital repository
- 3 hard copies for the library

PUBLICATION
Students are encouraged to publish at least one peer-reviewed paper before graduation. The university provides writing support and publication grants.

For research queries: research@university.edu.'''),

    # ========== 17. ACADEMIC ADVISING ==========
    ('Academic Advising Policy', 'Policy', '''PURPOSE
Academic advising supports students in making informed decisions about course selection, career pathways, and academic planning. Every student is assigned a faculty advisor on enrollment.

ADVISOR RESPONSIBILITIES
- Guide course selection based on degree requirements
- Monitor academic progress
- Discuss career and postgraduate plans
- Recommend support services when needed
- Sign off on registration forms, LOA requests, and graduation applications

STUDENT RESPONSIBILITIES
- Meet with advisor at least once per semester
- Come prepared with questions and a draft plan
- Follow through on advisor recommendations
- Notify advisor of changes in academic status or goals

MEETING SCHEDULE
- First semester: Initial orientation meeting
- Before each registration: 30-minute planning meeting
- Mid-semester: Optional check-in
- Before graduation: Final clearance meeting

Students who do not meet with their advisor may face a registration hold.

CHANGING ADVISORS
Students may request a different advisor if:
- The current advisor is unavailable for extended periods
- There is a professional conflict
- A different specialization aligns better with the student's goals

Change requests must be submitted to the Department Chair with a brief justification. Approvals typically take 1-2 weeks.

EARLY WARNING SYSTEM
If a student's CGPA drops below 2.5 or attendance below 75%, the advisor is automatically notified and must:
1. Schedule a meeting with the student.
2. Review the situation and identify causes.
3. Develop a plan (tutoring, reduced load, counseling).
4. Follow up within 4 weeks.

MENTAL HEALTH AND WELLBEING
Advisors are trained to recognize signs of stress, anxiety, and depression. When appropriate, advisors refer students to the Counseling Center. Confidentiality is respected within professional limits.

CAREER GUIDANCE
Advisors assist with:
- Internship search strategies
- CV and cover letter review
- Graduate school applications
- Industry connections

For advising-related queries: advising@university.edu.'''),

    # ========== 18. SEXUAL MISCONDUCT POLICY ==========
    ('Sexual Misconduct Policy', 'Policy', '''COMMITMENT
The university has zero tolerance for sexual misconduct including sexual harassment, sexual assault, dating violence, domestic violence, and stalking. This policy applies to all students, faculty, staff, and visitors.

DEFINITIONS
- Sexual Assault: Any non-consensual sexual contact or penetration.
- Consent: A clear, voluntary, mutually understandable agreement to engage in specific sexual activity. Silence or lack of resistance does not imply consent. Consent may be withdrawn at any time.
- Sexual Harassment: Unwelcome sexual advances, requests for favors, or other conduct of a sexual nature.
- Stalking: Repeated, unwanted attention that causes fear or distress.
- Dating Violence: Physical, sexual, or psychological harm by a current or former partner.

REPORTING OPTIONS
1. Confidential: Ombudsman, Counseling Center, Health Center
2. Formal: Title IX Coordinator, Dean of Students
3. Emergency: Campus Security or police
Anonymous reporting is available via the university's online portal.

The university will respect a complainant's choice about how to proceed, but may be legally required to investigate in some cases.

SUPPORT FOR COMPLAINANTS
- Immediate medical care
- Free counseling services
- Academic accommodations (class changes, extensions)
- Housing accommodations
- Legal aid referrals
- No-contact orders

INVESTIGATION PROCESS
1. Initial intake and safety planning.
2. Formal investigation by trained investigator.
3. Evidence reviewed by the Disciplinary Committee.
4. Hearing with both parties present (or separate, if requested).
5. Decision issued with sanctions and remedies.
6. Appeal available within 14 days.

STANDARD OF PROOF
The university uses the "preponderance of evidence" standard (more likely than not). This is the standard used by universities and does not replace criminal proceedings.

SANCTIONS
- Warning
- Educational requirements
- Counseling mandate
- Suspension
- Expulsion
- Referral to law enforcement

PREVENTION AND TRAINING
- All incoming students must complete online sexual misconduct prevention training.
- Annual training for faculty and staff is mandatory.
- Campus-wide awareness campaigns each semester.

CONFIDENTIALITY
Information is shared only on a need-to-know basis. Anonymous reports are investigated as far as possible without identifying the reporter.

For support or to report: titleix@university.edu or call the 24/7 hotline at (toll-free number).'''),

    # ========== 19. DISABILITY SERVICES ==========
    ('Disability Services Policy', 'Policy', '''COMMITMENT
The university is committed to providing equal educational opportunities to students with disabilities in compliance with applicable national and international laws.

ELIGIBILITY
Students with documented disabilities affecting mobility, vision, hearing, learning, mental health, chronic medical conditions, or other impairments are eligible for accommodations.

DISCLOSURE
Disclosure is voluntary. Students who wish to receive accommodations must:
1. Register with the Disability Services Office (DSO).
2. Provide documentation from a licensed professional.
3. Meet with a DSO counselor to discuss needs.

Documentation must be current (within 3 years) unless the disability is permanent.

COMMON ACCOMMODATIONS
- Extended exam time (typically 1.5x or 2x)
- Separate testing location
- Note-taking assistance
- Course material in accessible formats (large print, audio)
- Sign language interpreters
- Assistive technology
- Priority seating
- Flexibility with attendance for medical appointments
- Modified assignment deadlines in extenuating cases

ACADEMIC INTEGRITY
Accommodations do not compromise academic standards. Students are still responsible for demonstrating mastery of course content.

CONFIDENTIALITY
Disability information is confidential and shared only with individuals who need to implement accommodations.

FACULTY RESPONSIBILITIES
Faculty must:
- Include the accommodation statement in syllabi
- Implement approved accommodations confidentially
- Refer students to DSO if a need is disclosed
- Maintain respectful communication

STUDENT RESPONSIBILITIES
Students must:
- Request accommodations each semester (accommodations do not auto-renew)
- Notify faculty in advance
- Meet course requirements
- Communicate with DSO when issues arise

GRIEVANCES
Students who believe they have been denied accommodations may file a complaint with the DSO. If unresolved, complaints may be escalated to the Dean of Students.

TECHNOLOGY ACCESS
The university provides assistive technology at no cost, including:
- Screen readers
- Speech-to-text software
- Magnification tools
- Captioning services

For disability-related queries: dso@university.edu or Room B-215.'''),

    # ========== 20. GRADUATION REQUIREMENTS ==========
    ('Graduation Requirements and Procedures', 'Policy', '''DEGREE COMPLETION
To graduate, students must:
1. Complete all required credit hours for their program.
2. Maintain a minimum CGPA of 2.0 (undergraduate) or 3.0 (postgraduate).
3. Clear all financial obligations.
4. Return all university property (library books, lab equipment, etc.).
5. Submit a completed graduation application.

CREDIT HOUR REQUIREMENTS
- Bachelor's (Hons): 130-136 credit hours
- Bachelor's (Pass): 90-100 credit hours
- Master's (MS): 30-36 credit hours
- MPhil: 30 credit hours coursework + thesis
- PhD: 18 credit hours coursework + dissertation

RESIDENCY REQUIREMENT
- Undergraduate: Minimum 60 credit hours at this university.
- Postgraduate: Minimum 60% of coursework at this university.

GRADUATION APPLICATION
Applications must be submitted via the student portal by:
- Fall graduation: October 15
- Spring graduation: April 15
- Summer graduation: June 15

Late applications are accepted up to 15 days after the deadline with a PKR 5,000 late fee.

ELIGIBILITY CHECK
The Registrar's Office reviews:
- Academic record (all courses, grades, CGPA)
- Attendance record
- Disciplinary record
- Financial status

Students found deficient are notified 30 days before the convocation.

CLEARANCE PROCESS
Students must obtain clearance from:
- Library (no overdue books)
- Finance Office (no outstanding dues)
- Hostel (if resident)
- Department Chair (all coursework completed)

CLEARANCE FORM
The official clearance form must be signed by all parties and submitted to the Registrar.

CONVOCATION
- Annual convocation held in June/July
- Attendance is optional but encouraged
- Degree and transcript issued at convocation
- Non-attendees may collect degrees from Registrar's Office after the ceremony

DEGREE CLASSIFICATION
- First Class: CGPA 3.5-4.0
- Second Class (Upper): CGPA 3.0-3.49
- Second Class (Lower): CGPA 2.5-2.99
- Pass: CGPA 2.0-2.49

HONORS
- Cum Laude: CGPA 3.5+
- Magna Cum Laude: CGPA 3.7+
- Summa Cum Laude: CGPA 3.9+

TRANSCRIPT
Official transcripts are issued by the Registrar. Unofficial copies available on the student portal.

For graduation queries: registrar@university.edu.'''),
]


def main():
    db = SessionLocal()
    try:
        # English: Wipe existing documents and reseed with rich content.
        # Roman Urdu: Purane documents hata ke rich content ke saath dobara seed karo.
        existing = db.query(Document).filter(Document.tenant_id == TENANT_ID).all()
        print(f'Removing {len(existing)} existing documents...')
        for doc in existing:
            db.delete(doc)
        db.commit()

        print(f'Seeding {len(DOCUMENTS)} rich documents...')
        for title, category, content in DOCUMENTS:
            db.add(Document(
                tenant_id=TENANT_ID,
                title=title,
                category=category,
                content=content.strip(),
            ))
        db.commit()

        total = db.query(Document).count()
        print(f'\nDone. {total} documents in database.')

        # English: Show average word count per document.
        # Roman Urdu: Har document ke औसत words dikhao.
        docs = db.query(Document).all()
        total_words = sum(len(d.content.split()) for d in docs)
        avg = total_words // len(docs) if docs else 0
        print(f'Total words: {total_words}, Average per doc: {avg} words')
    finally:
        db.close()


if __name__ == '__main__':
    main()
