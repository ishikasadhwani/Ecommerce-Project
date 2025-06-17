import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_reset_email(to_email: str, token: str):
    subject = "Password Reset Request For Your Ecommerce Account"
    body = f"""
    Hi,

    We received a request to reset your password. Use the following token to reset your password:

    Token: {token}

    Note: This token is valid for 5 minutes.

    If you did not request this, you can safely ignore this email.

    Warm regards
    Support Team
    """

    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(message)
        print(f"Reset email sent to {to_email}")
    except Exception as e:
        print("Failed to send email:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send reset email. Please try again later.")
