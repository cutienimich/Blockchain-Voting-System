from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import RegisterRequest, TokenResponse
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# ─── REGISTER ────────────────────────────────────
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role="voter"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user_id": user.id}

# ─── LOGIN ───────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # username field = email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}

from app.email_utils import send_otp_email
from app.utils import generate_otp, verify_otp
from app.schemas import OTPRequest, OTPVerify

# ─── REQUEST OTP ─────────────────────────────────
@router.post("/request-otp")
async def request_otp(data: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    otp = generate_otp(data.email)
    await send_otp_email(data.email, otp)
    return {"message": "OTP sent to your email!"}

# ─── VERIFY OTP ──────────────────────────────────
@router.post("/verify-otp")
def verify_otp_route(data: OTPVerify):
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "Email verified! You may now login."}
