from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME   = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD   = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM       = os.getenv("MAIL_FROM"),
    MAIL_PORT       = 587,
    MAIL_SERVER     = "smtp.gmail.com",
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS  = False   # ← dagdag lang ito
)

async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="Your E-Voting OTP Code",
        recipients=[email],
        body=f"""
            <h3>E-Voting System - Email Verification</h3>
            <p>Your OTP code is: <strong>{otp}</strong></p>
            <p>This code expires in <strong>10 minutes</strong>.</p>
            <p>If you did not request this, ignore this email.</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)