from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─── PASSWORD ────────────────────────────────────
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

# ─── JWT TOKEN ───────────────────────────────────
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

import random, string
from datetime import datetime, timedelta

# ─── OTP ─────────────────────────────────────────
otp_store = {}  # { email: { otp, expires } }

def generate_otp(email: str) -> str:
    otp = "".join(random.choices(string.digits, k=6))
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    return otp

def verify_otp(email: str, otp_input: str) -> bool:
    record = otp_store.get(email)
    if not record:
        return False
    if datetime.utcnow() > record["expires"]:
        del otp_store[email]
        return False
    if record["otp"] != otp_input:
        return False
    del otp_store[email]
    return True