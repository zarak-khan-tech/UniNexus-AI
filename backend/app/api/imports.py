"""
English: CSV import endpoints — bulk-add students, courses, enrollments.
         Admin-only. Validates input, handles duplicates, returns a summary.
Roman Urdu: CSV import endpoints — students, courses, enrollments bulk add.
            Sirf admin. Validation, duplicates, summary return.
"""
import csv
import io
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/import', tags=['Imports'])

MAX_CSV_BYTES = 2 * 1024 * 1024  # 2 MB


def _read_csv(content: bytes) -> List[Dict[str, str]]:
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('latin-1')
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


async def _load_csv(file: UploadFile) -> List[Dict[str, str]]:
    """English: Common upload + parse + size guard.
    Roman Urdu: Common upload + parse + size guard."""
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='File must be a .csv')
    content = await file.read()
    if len(content) > MAX_CSV_BYTES:
        raise HTTPException(status_code=413, detail=f'CSV too large (max {MAX_CSV_BYTES // 1024} KB)')
    try:
        return _read_csv(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Could not parse CSV: {e}')


def _summary(added: int, skipped: int, errors: List[str]) -> str:
    parts = [f'{added} added', f'{skipped} skipped']
    if errors:
        parts.append(f'{len(errors)} error(s)')
    return ', '.join(parts)


# =============================================================================
# Students
# =============================================================================
@router.post('/students')
async def import_students(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    rows = await _load_csv(file)
    if not rows:
        return {'ok': True, 'added': 0, 'skipped': 0, 'errors': [], 'summary': 'No rows found.'}

    added = skipped = 0
    errors: List[str] = []

    for i, row in enumerate(rows, start=2):
        num = (row.get('student_number') or '').strip()
        first = (row.get('first_name') or '').strip()
        last = (row.get('last_name') or '').strip()
        email = (row.get('email') or '').strip().lower()
        year_raw = (row.get('enrollment_year') or '').strip()

        if not num or not first or not last or not email or not year_raw:
            errors.append(f'Row {i}: missing required field(s)')
            continue
        if '@' not in email:
            errors.append(f'Row {i}: invalid email "{email}"')
            continue
        try:
            year = int(year_raw)
        except ValueError:
            errors.append(f'Row {i}: invalid enrollment_year "{year_raw}"')
            continue

        existing = db.query(Student).filter(
            Student.tenant_id == current_user.tenant_id,
            ((Student.student_number == num) | (Student.email == email)),
        ).first()
        if existing:
            skipped += 1
            continue

        try:
            db.add(Student(
                tenant_id=current_user.tenant_id, student_number=num,
                first_name=first, last_name=last, email=email, enrollment_year=year,
            ))
            db.commit()
            added += 1
        except Exception as e:
            db.rollback()
            errors.append(f'Row {i}: {str(e)[:120]}')

    return {'ok': True, 'added': added, 'skipped': skipped,
            'errors': errors[:20], 'summary': _summary(added, skipped, errors)}


# =============================================================================
# Courses
# =============================================================================
@router.post('/courses')
async def import_courses(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    """
    English: Import courses from CSV: course_code, title, credit_hours, department
    Roman Urdu: CSV se courses import karo: course_code, title, credit_hours, department
    """
    rows = await _load_csv(file)
    if not rows:
        return {'ok': True, 'added': 0, 'skipped': 0, 'errors': [], 'summary': 'No rows found.'}

    added = skipped = 0
    errors: List[str] = []

    for i, row in enumerate(rows, start=2):
        code = (row.get('course_code') or '').strip().upper()
        title = (row.get('title') or '').strip()
        hours_raw = (row.get('credit_hours') or '').strip()
        dept = (row.get('department') or '').strip()

        if not code or not title or not hours_raw or not dept:
            errors.append(f'Row {i}: missing required field(s)')
            continue
        try:
            hours = int(hours_raw)
            if hours < 1 or hours > 10:
                errors.append(f'Row {i}: credit_hours out of range (1-10): {hours}')
                continue
        except ValueError:
            errors.append(f'Row {i}: invalid credit_hours "{hours_raw}"')
            continue

        existing = db.query(Course).filter(
            Course.tenant_id == current_user.tenant_id,
            Course.course_code == code,
        ).first()
        if existing:
            skipped += 1
            continue

        try:
            db.add(Course(
                tenant_id=current_user.tenant_id, course_code=code,
                title=title, credit_hours=hours, department=dept,
            ))
            db.commit()
            added += 1
        except Exception as e:
            db.rollback()
            errors.append(f'Row {i}: {str(e)[:120]}')

    return {'ok': True, 'added': added, 'skipped': skipped,
            'errors': errors[:20], 'summary': _summary(added, skipped, errors)}


# =============================================================================
# Enrollments
# =============================================================================
@router.post('/enrollments')
async def import_enrollments(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    """
    English: Import enrollments from CSV: student_number, course_code, grade, attendance_percentage
    Roman Urdu: CSV se enrollments import karo: student_number, course_code, grade, attendance_percentage
    """
    rows = await _load_csv(file)
    if not rows:
        return {'ok': True, 'added': 0, 'skipped': 0, 'errors': [], 'summary': 'No rows found.'}

    added = skipped = 0
    errors: List[str] = []

    for i, row in enumerate(rows, start=2):
        snum = (row.get('student_number') or '').strip()
        ccode = (row.get('course_code') or '').strip().upper()
        grade = (row.get('grade') or '').strip().upper() or None
        att_raw = (row.get('attendance_percentage') or '').strip()

        if not snum or not ccode or not att_raw:
            errors.append(f'Row {i}: missing required field(s)')
            continue
        try:
            att = float(att_raw)
            if att < 0 or att > 100:
                errors.append(f'Row {i}: attendance_percentage out of range (0-100): {att}')
                continue
        except ValueError:
            errors.append(f'Row {i}: invalid attendance_percentage "{att_raw}"')
            continue

        student = db.query(Student).filter(
            Student.tenant_id == current_user.tenant_id,
            Student.student_number == snum,
        ).first()
        if not student:
            errors.append(f'Row {i}: student_number "{snum}" not found')
            continue

        course = db.query(Course).filter(
            Course.tenant_id == current_user.tenant_id,
            Course.course_code == ccode,
        ).first()
        if not course:
            errors.append(f'Row {i}: course_code "{ccode}" not found')
            continue

        existing = db.query(Enrollment).filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id,
        ).first()
        if existing:
            skipped += 1
            continue

        try:
            db.add(Enrollment(
                student_id=student.id, course_id=course.id,
                grade=grade, attendance_percentage=att,
            ))
            db.commit()
            added += 1
        except Exception as e:
            db.rollback()
            errors.append(f'Row {i}: {str(e)[:120]}')

    return {'ok': True, 'added': added, 'skipped': skipped,
            'errors': errors[:20], 'summary': _summary(added, skipped, errors)}
