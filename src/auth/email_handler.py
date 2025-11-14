import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()  # para leer variables del .env

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM", "no-reply@hospital.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 2525)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_reset_email(email: EmailStr, token: str):
    reset_link = f"http://localhost:4200/auth/reset-password?token={token}"
    html = f"""
    <p>Hola,</p>
    <p>Has solicitado restablecer tu contraseña.</p>
    <p><a href="{reset_link}">Haz clic aquí para crear una nueva contraseña</a></p>
    <p>Este enlace expirará en 15 minutos.</p>
    <p>Si no hiciste esta solicitud, ignora este mensaje.</p>
    """
    message = MessageSchema(
        subject="Restablecer contraseña - Hospital Salud",
        recipients=[email],
        body=html,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
