# logic/utils/email_utils.py
import smtplib
from email.message import EmailMessage
from typing import List, Optional

def send_email(
    subject: str,
    body: str,
    to_emails: List[str],
    from_email: str,
    from_email_password: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    reply_to: Optional[str] = None
) -> bool:
    """
    Send an email using SMTP.

    Args:
        subject: Subject of the email.
        body: Body content of the email.
        to_emails: List of recipient email addresses.
        from_email: Sender email address.
        from_email_password: Sender email password or app password.
        smtp_server: SMTP server address (default: Gmail).
        smtp_port: SMTP server port (default: 587 for TLS).
        reply_to: Optional reply-to email.

    Returns:
        True if email sent successfully, False otherwise.
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_email_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
