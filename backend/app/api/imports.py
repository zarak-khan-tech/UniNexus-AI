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

# English: Hard limit so a bad upload can't exhaust memory.
# Roman Urdu: Hard limit taake kharab upload memory na khatam kar de.
MAX_CSV_BYTES = 2 * 1024 * 1024  # 2 MB


def _read_csv(content: bytes) -> List[Dict[str, str]]:
    """English: Decode CSV bytes into a list of row dicts.
    Roman Urdu: CSV bytes ko row dicts ki list mein decode karo."""
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('latin-1')
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


@router.post('/students')
async def import_students(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    """
    English: Import students from a CSV file with columns:
             student_number, first_name, last_name, email, enrollment_year
    Roman Urdu: CSV file se students import karo. Columns:
                student_number, first_name, last_name, email, enrollment_year
    """
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='File must be a .csv')

    content = await file.read()
    if len(content) > MAX_CSV_BYTES:
        raise HTTPException(status_code=413, detail=f'CSV too large (max {MAX_CSV_BYTES // 1024} KB)')

    try:
        rows = _read_csv(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Could not parse CSV: {e}')

    if not rows:
        return {'ok': True, 'added': 0, 'skipped': 0, 'errors': [], 'summary': 'No rows found.'}

    added = 0
    skipped = 0
    errors: List[str] = []

    for i, row in enumerate(rows, start=2):  # start=2 because row 1 is header
        num = (row.get('student_number') or '').strip()
        first = (row.get('first_name') or '').strip()
        last = (row.get('last_name') or '').strip()
        email = (row.get('email') or '').strip().lower()
        year_raw = (row.get('enrollment_year') or '').strip()

        # English: Validate required fields.
        # Roman Urdu: Required fields validate karo.
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

        # English: Check duplicates by student_number OR email within this tenant.
        # Roman Urdu: Iss tenant mein student_number ya email duplicate check.
        existing = db.query(Student).filter(
            Student.tenant_id == current_user.tenant_id,
            ((Student.student_number == num) | (Student.email == email)),
        ).first()

        if existing:
            skipped += 1
            continue

        try:
            db.add(Student(
                tenant_id=current_user.tenant_id,
                student_number=num,
                first_name=first,
                last_name=last,
                email=email,
                enrollment_year=year,
            ))
            db.commit()
            added += 1
        except Exception as e:
            db.rollback()
            errors.append(f'Row {i}: {str(e)[:120]}')

    summary_parts = [f'{added} added', f'{skipped} skipped']
    if errors:
        summary_parts.append(f'{len(errors)} error(s)')
    return {
        'ok': True,
        'added': added,
        'skipped': skipped,
        'errors': errors[:20],  # English: cap at 20 for readability.
        'summary': ', '.join(summary_parts),
    }
