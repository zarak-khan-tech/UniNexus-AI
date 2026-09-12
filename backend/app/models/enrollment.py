from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grade = Column(String, nullable=True) # e.g., A, B+, C
    attendance_percentage = Column(Float, default=100.0)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
