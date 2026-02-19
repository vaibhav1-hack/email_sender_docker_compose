import os
import time
import smtplib
from email.message import EmailMessage
from typing import List, Dict, Any
from dotenv import load_dotenv
from typing import Optional
load_dotenv()


def _env(name: str, default: Optional[str] = None) -> str:

    val = os.environ.get(name, default)
    if not val:
        raise ValueError(f"Missing environment variable: {name}")
    return val


def send_bulk_emails(recipients: List[str], delay_seconds: int = 10) -> Dict[str, Any]:
    """
    Sends 'hi this is vaibhav' to each recipient with delay.
    SMTP config is taken from environment variables:
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM (optional), SMTP_SUBJECT (optional)
    """
    # Validate and clean recipients
    cleaned = []
    for r in recipients:
        r = (r or "").strip()
        if r and "@" in r:
            cleaned.append(r)

    if not cleaned:
        raise ValueError("No valid email addresses provided.")

    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    smtp_from = os.environ.get("SMTP_FROM","SMTP_USER")

    #TO_EMAIL  = "vaibhavswarnkar281@gmail.com"
    subject =  os.environ.get("SMTP_SUBJECT")
    body = "hi this is vaibhav from docker container"

    results = {"sent": [], "failed": []}

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)

        for idx, to_email in enumerate(cleaned, start=1):
            msg = EmailMessage()
            msg["From"] = "boathack0@gmail.com"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body)

            try:
                server.send_message(msg)
                results["sent"].append(to_email)
            except Exception as e:
                results["failed"].append({"email": to_email, "error": str(e)})

            # Delay between sends (except after last)
            if idx < len(cleaned):
                time.sleep(delay_seconds)

    return results


if __name__ == "__main__":
    # Optional CLI usage (not required for UI):
    # set EMAILS="a@x.com,b@y.com" then run python send_mail_update.py
    emails = os.environ.get("EMAILS", "")
    recipients = [e.strip() for e in emails.replace("\n", ",").split(",") if e.strip()]
    out = send_bulk_emails(recipients, delay_seconds=int(os.environ.get("DELAY", "10")))
    print(out)

