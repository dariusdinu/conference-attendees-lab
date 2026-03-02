from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class AttendeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    is_active: bool = True

class AttendeeCreate(AttendeeBase):
    pass

class AttendeeUpdatePut(AttendeeBase):
    pass

class AttendeeUpdatePatch(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    is_active: bool | None = None

class AttendeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True