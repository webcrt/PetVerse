# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional

# Gmail SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "achu50002@gmail.com"
SMTP_PASSWORD = "yirp sdwp eidn xubt"  # Use Gmail App Password, not your real password!


def send_email(to: str, subject: str, text: Optional[str] = None, html: Optional[str] = None, cc: Optional[str] = None) -> Dict[str, str]:
    """Send email using Gmail SMTP"""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_USERNAME
        msg["To"] = to
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = cc

        if text:
            msg.attach(MIMEText(text, "plain"))
        if html:
            msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [to], msg.as_string())

        print(f"✅ Email sent to {to}")
        return {"status": "success", "to": to}

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return {"status": "error", "message": str(e)}


def send_feeding_reminder(owner_email: str, pet_name: str, food_type: Optional[str], amount: Optional[str], reminder_time: str):
    """Send feeding reminder email"""
    subject = f"🍽️ Feeding time for {pet_name}!"
    text = f"""
Hi there!

It's feeding time for {pet_name}!

Reminder Details:
- Time: {reminder_time}
- Food Type: {food_type or 'Not specified'}
- Amount: {amount or 'Not specified'}

Don't forget to give your furry friend some love along with their meal! 🐾

Best regards,
Pet Care Connect
    """
    return send_email(owner_email, subject, text)

def send_vaccination_reminder(owner_email, pet_name, vaccine_name, vaccination_date, notes=None):
    subject = f"💉 Vaccination Reminder for {pet_name}"
    text = f"""
Hello,

This is a reminder for your pet's vaccination.

Pet Name: {pet_name}
Vaccine: {vaccine_name}
Date: {vaccination_date}

Notes: {notes or 'No additional notes'}

Please ensure timely vaccination to keep your pet healthy 🐾

Regards,
Pet Care Connect
    """
    return send_email(owner_email, subject, text)


def send_adoption_application_notification(agency_email: str, applicant_name: str, pet_name: str, application_id: int):
    subject = f"New Adoption Application for {pet_name}"
    text = f"""
Hello,

You have received a new adoption application from {applicant_name} for {pet_name}.

Application ID: #{application_id}

Best regards,
Pet Care Connect Team
    """
    return send_email(agency_email, subject, text)


def send_application_response_notification(applicant_email: str, pet_name: str, status: str, agency_notes: Optional[str] = None):
    if status == 'approved':
        subject = f"✅ Adoption Approved for {pet_name}"
        text = f"""
Congratulations!

Your adoption application for {pet_name} has been APPROVED!

Agency Notes: {agency_notes or 'None'}

Best regards,
Pet Care Connect Team
        """
    else:
        subject = f"ℹ️ Update on your adoption application for {pet_name}"
        text = f"""
Thank you for your interest in adopting {pet_name}.
Unfortunately, your application was not selected.

Agency Notes: {agency_notes or 'None'}

Don't give up—there are many pets waiting for loving homes.

Best regards,
Pet Care Connect Team
        """
    return send_email(applicant_email, subject, text)


def send_order_confirmation(customer_email: str, order_number: str, total_amount: float, items: List[Dict]):
    subject = f"Order Confirmation - #{order_number}"
    items_text = "\n".join([f"- {item['name']} x{item['quantity']} - ₹{item['price']:.2f}" for item in items])

    text = f"""
Thank you for your order!

Order Number: #{order_number}
Total: ₹{total_amount:.2f}

Items Ordered:
{items_text}

Your order is being processed and you'll receive tracking information soon.

Best regards,
Pet Care Connect Team
    """
    return send_email(customer_email, subject, text)
