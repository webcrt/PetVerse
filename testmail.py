# test_email.py
from email_utils import send_email   # <-- adjust if your function is inside app.py instead

if __name__ == "__main__":
    # Change this to your personal email where you want to receive the test
    recipient = "aswanas315@gmail.com"

    result = send_email(
        to=recipient,
        subject="✅ Test Email from PetCareConnect",
        text="Hello!\n\nThis is a test email sent from your Flask project using Gmail SMTP.\n\nIf you received this, your email setup works! 🚀"
    )

    print("Result:", result)
