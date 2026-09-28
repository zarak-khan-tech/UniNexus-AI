"""
English: Tool package initializer. Registers all tools on import.
Roman Urdu: Tool package initializer. Import pe sab tools register karta hai.
"""
from backend.app.tools.registry import tool_registry
from backend.app.tools.academic import (
    StudentLookupTool,
    ListStudentsTool,
    AttendanceQueryTool,
    ListEnrollmentsTool,
)
from backend.app.tools.knowledge import SemanticSearchTool
from backend.app.tools.write import UpdateStudentGradeTool, SendStudentNotificationTool

for _tool_cls in (
    StudentLookupTool, ListStudentsTool, AttendanceQueryTool, ListEnrollmentsTool,
    SemanticSearchTool,
    UpdateStudentGradeTool, SendStudentNotificationTool,
):
    tool_registry.register(_tool_cls())

__all__ = ['tool_registry']
