import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmailConfigError(Exception):
    """Raised when email configuration is invalid or incomplete."""
    pass


def _get_smtp_config():
    """Load SMTP configuration from environment variables."""
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM", user)
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"}

    if not host or not user or not password or not from_email:
        raise EmailConfigError(
            "SMTP configuration is incomplete. Please set SMTP_HOST, SMTP_PORT, "
            "SMTP_USER, SMTP_PASSWORD and SMTP_FROM in your environment."
        )

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_email": from_email,
        "use_tls": use_tls,
    }


def send_email(to_email: str, subject: str, html_body: str, text_body: str | None = None) -> None:
    """Send an HTML email using SMTP configuration from environment variables.

    :param to_email: Recipient email address
    :param subject: Email subject
    :param html_body: HTML body content
    :param text_body: Optional plain-text alternative
    :raises EmailConfigError: if SMTP configuration is invalid
    :raises smtplib.SMTPException: for SMTP related errors
    """
    config = _get_smtp_config()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config["from_email"]
    msg["To"] = to_email

    # Fallback text body
    if not text_body:
        text_body = "Tu carta de Amigo Secreto está disponible en formato HTML."

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(config["host"], config["port"]) as smtp:
        if config["use_tls"]:
            smtp.starttls()
        smtp.login(config["user"], config["password"])
        smtp.send_message(msg)
