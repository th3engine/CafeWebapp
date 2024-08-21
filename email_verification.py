from itsdangerous import URLSafeTimedSerializer,SignatureExpired,BadSignature
from flask import render_template, url_for
import os
from smtplib import SMTP, SMTPResponseException


def generate_token(email):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
        return email
    except (SignatureExpired,BadSignature):
        return False