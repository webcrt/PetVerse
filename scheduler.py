# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from models import db, Pet, FeedingReminder
from email_utils import send_feeding_reminder
from datetime import datetime
from zoneinfo import ZoneInfo
from models import VaccinationReminder, User
from email_utils import send_vaccination_reminder
from datetime import date

# Use Indian timezone
LOCAL_TZ = ZoneInfo("Asia/Kolkata")

scheduler = BackgroundScheduler(timezone=LOCAL_TZ)


def schedule_pet_feeding_jobs(app):
    """Schedule all feeding reminder jobs from database."""
    with app.app_context():
        # Remove old jobs to avoid duplicates
        scheduler.remove_all_jobs()

        pets = Pet.query.all()

        for pet in pets:
            reminders = FeedingReminder.query.filter_by(
                pet_id=pet.id,
                is_active=True
            ).all()

            for reminder in reminders:
                try:
                    # Normalize time input (fix 12.00 PM → 12:00 PM)
                    raw_time = reminder.reminder_time.strip().replace(".", ":")

                    # Detect format
                    if "AM" in raw_time.upper() or "PM" in raw_time.upper():
                        reminder_time = datetime.strptime(
                            raw_time, "%I:%M %p"
                        ).time()
                    else:
                        reminder_time = datetime.strptime(
                            raw_time, "%H:%M"
                        ).time()

                    formatted_time = reminder_time.strftime("%I:%M %p")

                    job_id = f"feeding_{pet.id}_{reminder.id}"

                    current_app.logger.info(
                        f"⏰ Scheduling Feeding Reminder | Job={job_id} | "
                        f"Time={formatted_time}"
                    )

                    scheduler.add_job(
                        func=send_feeding_reminder,
                        trigger="cron",
                        id=job_id,
                        hour=reminder_time.hour,
                        minute=reminder_time.minute,
                        args=[
                            pet.owner.email,
                            pet.name,
                            reminder.food_type,
                            reminder.amount,
                            formatted_time,
                        ],
                        replace_existing=True,
                    )

                except Exception as e:
                    current_app.logger.error(
                        f"❌ Failed to schedule reminder {reminder.id}: {e}"
                    )

        # Debug all jobs
        for job in scheduler.get_jobs():
            current_app.logger.info(
                f"📌 Job Active: {job.id} → {job.trigger}"
            )

        current_app.logger.info("✅ Feeding reminders scheduled successfully.")

def check_and_send_vaccination_reminders(app):
    """Send vaccination reminder emails on due date."""
    with app.app_context():
        today = date.today()

        reminders = VaccinationReminder.query.filter(
            VaccinationReminder.is_active == True,
            VaccinationReminder.vaccination_date == today,
            VaccinationReminder.last_sent == None
        ).all()

        for reminder in reminders:
            user = User.query.get(reminder.owner_id)

            current_app.logger.info(
                f"💉 Sending vaccination reminder | Pet={reminder.pet.name} | "
                f"Vaccine={reminder.vaccine_name}"
            )

            send_vaccination_reminder(
                owner_email=user.email,
                pet_name=reminder.pet.name,
                vaccine_name=reminder.vaccine_name,
                vaccination_date=reminder.vaccination_date.strftime("%d %b %Y"),
                notes=reminder.notes
            )

            reminder.last_sent = datetime.utcnow()
            db.session.commit()

def schedule_vaccination_jobs(app):
    """Daily vaccination reminder checker."""
    scheduler.add_job(
        func=check_and_send_vaccination_reminders,
        trigger="interval",
        minutes=1,
        args=[app],
        id="vaccination_reminder_job",
        replace_existing=True,
    )
              