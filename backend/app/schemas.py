from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ─── AUTH SCHEMAS ────────────────────────────────
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ─── ELECTION SCHEMAS ────────────────────────────
class ElectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class ElectionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    is_active: bool

    class Config:
        from_attributes = True

# ─── CANDIDATE SCHEMAS ───────────────────────────
class CandidateCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CandidateResponse(BaseModel):
    id: int
    election_id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
        
# ─── VOTE SCHEMAS ────────────────────────────────
class VoteCreate(BaseModel):
    election_id: int
    candidate_id: int

class VoteResponse(BaseModel):
    id: int
    user_id: int
    election_id: int
    candidate_id: int
    transaction_hash: Optional[str]
    is_flagged: bool

    class Config:
        from_attributes = True


# ─── OTP SCHEMAS ─────────────────────────────────
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str