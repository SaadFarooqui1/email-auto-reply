import imaplib
import smtplib
import email
from email.message import EmailMessage

# Email Credentials
IMAP_SERVER = "add your hostings imap server"
SMTP_SERVER = "add smtp server"
EMAIL_ADDRESS = "john@example.com"
EMAIL_PASSWORD = "your password"

# Keywords to identify job applications
JOB_KEYWORDS = ["job application", "application for", "applying for", "resume", "cv",
    "cover letter", "job posting", "job ID", "position", "role", "vacancy",
    "job opening", "career opportunity", "employment opportunity", "job inquiry",
    "application submission", "application for employment", "job application for",
    "resume submission", "cv submission", "application submission for", "job interest",
    "application for position", "candidate application", "job application submission",
    "application for Graphic Designer", "Graphic Designer application",
    "application for WordPress Developer", "WordPress Developer application",
    "application for Human Resources", "Human Resources application",
    "application for HR", "HR application",
    "application for Full Stack Developer", "Full Stack Developer application"]

def check_emails():
    """Check unread emails for job applications"""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select("inbox")

    # Search for unread emails
    result, data = mail.search(None, "UNSEEN")
    email_ids = data[0].split()

    for e_id in email_ids:
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["subject"]
                sender = msg["from"]

                # Check if email contains job-related keywords
                if any(keyword.lower() in subject.lower() for keyword in JOB_KEYWORDS):
                    print(f"Job Application detected from {sender}, sending auto-reply...")
                    send_auto_reply(sender)

    mail.logout()

def send_auto_reply(to_email):
    """Send an auto-reply to the sender"""
    msg = EmailMessage()
    msg["Subject"] = "Re: Your Job Application"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(
        "Dear Applicant,\n\n"
        "Thank you for reaching out! We have received your job application and will review it soon. "
        "If your qualifications match our needs, we will contact you.\n\n"
        "Best regards,\nHR Team"
    )

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Auto-reply sent to {to_email}")

# Run the script
check_emails()
