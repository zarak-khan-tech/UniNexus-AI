"""
English: Document upload API — admin-only. Accepts .txt, .md files. Optionally
.pdf if pypdf is installed.
Roman Urdu: Document upload API — sirf admin. .txt, .md files accept karta 
hai. Agar pypdf installed ho to .pdf bhi.
"""
import io
import logging
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.document import Document
from backend.app.services.document_ingest import ingest_document

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/documents', tags=['Documents'])

# English: Max upload size — 2 MB (matches CSV import).
# Roman Urdu: Max upload size — 2 MB (CSV import jaisa).
MAX_BYTES = 2 * 1024 * 1024


def _extract_text_from_upload(filename: str, content: bytes) -> str:
    """English: Extract plain text based on the file extension.
    Roman Urdu: File extension ke hisaab se plain text nikaalo."""
    lower = (filename or '').lower()
    if lower.endswith('.txt') or lower.endswith('.md'):
        try:
            return content.decode('utf-8-sig')
        except UnicodeDecodeError:
            return content.decode('latin-1')
    if lower.endswith('.pdf'):
        try:
            from pypdf import PdfReader  # optional
        except ImportError:
            raise HTTPException(
                status_code=400,
                detail='PDF support not installed. Run: pip install pypdf',
            )
        try:
            reader = PdfReader(io.BytesIO(content))
            return '\n\n'.join((page.extract_text() or '') for page in reader.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Could not read PDF: {e}')
    raise HTTPException(
        status_code=400,
        detail='Unsupported file type. Use .txt, .md, or .pdf.',
    )


@router.post('/upload')
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form('Policy'),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    """
    English: Upload a document, chunk it, embed, and store in the knowledge 
    base.
    Roman Urdu: Document upload karo, chunk karo, embed karo, aur knowledge 
    base mein store karo.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file provided')
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f'File too large (max {MAX_BYTES // 1024} KB)')

    text = _extract_text_from_upload(file.filename, content)
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail='No text content extracted from file')

    # English: Reject duplicate titles for the same tenant.
    # Roman Urdu: Same tenant ke liye duplicate titles reject karo.
    existing = db.query(Document).filter(
        Document.tenant_id == current_user.tenant_id,
        Document.title == title,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail=f'A document titled "{title}" already exists')

    summary = ingest_document(
        tenant_id=current_user.tenant_id,
        title=title,
        category=category,
        content=text,
    )
    return {'ok': True, **summary}
