# Referenced from replitmail integration
import os
import requests
import json
from typing import List, Optional, Dict, Any

def get_auth_token():
    """Get Replit authentication token"""
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    if repl_identity:
        return f"repl {repl_identity}"
    elif web_repl_renewal:
        return f"depl {web_repl_renewal}"
    else:
        raise ValueError("No authentication token found. Please ensure you're running in Replit environment.")

def send_email(to: str, subject: str, text: Optional[str] = None, html: Optional[str] = None, cc: Optional[str] = None) -> Dict[str, Any]:
    """Send email using Replit's mail service"""
    try:
        auth_token = get_auth_token()
        
        payload = {
            "to": to,
            "subject": subject
        }
        
        if cc:
            payload["cc"] = cc
        if text:
            payload["text"] = text
        if html:
            payload["html"] = html
            
        response = requests.post(
            "https://connectors.replit.com/api/v2/mailer/send",
            headers={
                "Content-Type": "application/json",
                "X_REPLIT_TOKEN": auth_token,
            },
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Email sending failed: {response.status_code} - {response.text}")
            return {"error": "Failed to send email"}
            
    except Exception as e:
        print(f"Email error: {str(e)}")
        return {"error": str(e)}

def send_adoption_application_notification(agency_email: str, applicant_name: str, pet_name: str, application_id: int):
    """Send notification to agency about new adoption application"""
    subject = f"New Adoption Application for {pet_name}"
    text = f"""
Hello,

You have received a new adoption application from {applicant_name} for {pet_name}.

Please log in to your dashboard to review the application details and respond.

Application ID: #{application_id}

Best regards,
Pet Care Connect Team
    """
    
    return send_email(agency_email, subject, text)

def send_application_response_notification(applicant_email: str, pet_name: str, status: str, agency_notes: Optional[str] = None):
    """Send notification to applicant about application status"""
    if status == 'approved':
        subject = f"Great News! Your adoption application for {pet_name} has been approved"
        text = f"""
Congratulations!

Your adoption application for {pet_name} has been APPROVED!

The adoption agency will contact you soon to arrange the next steps.

{f'Agency Notes: {agency_notes}' if agency_notes else ''}

Best regards,
Pet Care Connect Team
        """
    else:
        subject = f"Update on your adoption application for {pet_name}"
        text = f"""
Thank you for your interest in adopting {pet_name}.

Unfortunately, your application was not selected this time. 

{f'Agency Notes: {agency_notes}' if agency_notes else ''}

Don't give up! There are many wonderful pets waiting for loving homes.

Best regards,
Pet Care Connect Team
        """
    
    return send_email(applicant_email, subject, text)

def send_feeding_reminder(owner_email: str, pet_name: str, food_type: Optional[str], amount: Optional[str], reminder_time: str):
    """Send feeding reminder email"""
    subject = f"🍽️ Feeding time for {pet_name}!"
    text = f"""
Hi there!

It's feeding time for {pet_name}!

Reminder Details:
- Time: {reminder_time}
- Food Type: {food_type}
- Amount: {amount}

Don't forget to give your furry friend some love along with their meal! 🐾

Best regards,
Pet Care Connect
    """
    
    return send_email(owner_email, subject, text)

def send_order_confirmation(customer_email: str, order_number: str, total_amount: float, items: List[Dict]):
    """Send order confirmation email"""
    subject = f"Order Confirmation - #{order_number}"
    
    items_text = "\n".join([f"- {item['name']} x{item['quantity']} - ${item['price']:.2f}" for item in items])
    
    text = f"""
Thank you for your order!

Order Number: #{order_number}
Total: ${total_amount:.2f}

Items Ordered:
{items_text}

Your order is being processed and you'll receive tracking information soon.

Best regards,
Pet Care Connect Team
    """
    
    return send_email(customer_email, subject, text)