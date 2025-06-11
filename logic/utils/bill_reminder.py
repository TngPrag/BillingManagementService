# logic/utils/bill_reminders.py
import asyncio
from logic.utils.email_utils import send_email
from datetime import datetime, timedelta

async def schedule_bill_reminders(due_date: datetime, customer_email: str, bill_description: str, from_email: str, from_password: str):
    now = datetime.utcnow()
    reminders = [
        (due_date - timedelta(days=3), "Upcoming Bill Reminder (3 days)"),
        (due_date - timedelta(days=1), "Upcoming Bill Reminder (1 day)"),
        (due_date, "Your Bill is Due Today"),
    ]

    for send_time, subject in reminders:
        delay = (send_time - now).total_seconds()
        if delay > 0:
            await asyncio.sleep(delay)
        send_email(
            subject=subject,
            body=f"Reminder: {bill_description} is due on {due_date.strftime('%Y-%m-%d')}",
            to_emails=[customer_email],
            from_email=from_email,
            from_email_password=from_password
        )
