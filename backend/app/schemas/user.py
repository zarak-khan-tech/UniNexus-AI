from pydantic import BaseModel, EmailStr
from datetime import datetime

# Tenant Schemas
class TenantBase(BaseModel):
    name: str
    domain: str

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str = "student"

class UserCreate(UserBase):
    password: str
    tenant_id: int

class UserResponse(UserBase):
    id: int
    tenant_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
