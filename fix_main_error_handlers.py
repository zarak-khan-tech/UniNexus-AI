"""
English: Register global error handlers in main.py (idempotent).
Roman Urdu: main.py mein global error handlers register karo (idempotent).
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "register_error_handlers" in content or "add_exception_handler" in content:
    print("SKIP: error handlers already registered")
    raise SystemExit(0)

anchor = "app.add_middleware(\n    CORSMiddleware,"
if anchor not in content:
    print("ERROR: middleware anchor not found")
    raise SystemExit(1)

addition = """# English: Register global error handlers for consistent API responses.
# Roman Urdu: Consistent API responses ke liye global error handlers register karo.
from backend.app.core.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


app.add_middleware(
    CORSMiddleware,"""

content = content.replace(anchor, addition, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: error handlers registered in main.py")
