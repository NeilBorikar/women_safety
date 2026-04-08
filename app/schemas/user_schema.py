from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
import re


# 📞 Emergency Contact

class EmergencyContact(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    relation: Optional[str] = Field(None, max_length=30)



# 🔐 User Register

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    emergency_contacts: Optional[List[EmergencyContact]] = None

    @field_validator("password")
    def validate_password(cls, v):
        # Strong password policy
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")

        return v


# 🔑 Login

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ✏️ Update User

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)


# ➕ Add Emergency Contact

class AddEmergencyContact(BaseModel):
    contact: EmergencyContact


# 📤 Response Schema

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    emergency_contacts: List[EmergencyContact] = []


# 🔐 Token Response

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"