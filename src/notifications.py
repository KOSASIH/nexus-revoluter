import logging
from typing import List, Dict, Any
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client as TwilioClient
import asyncio
from jinja2 import Template

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationService:
    def __init__(self, email_config: Dict[str, str], sms_config: Dict[str, str]):
        self.email_config = email_config
        self.sms_config = sms_config
        self.twilio_client = TwilioClient(sms_config['account_sid'], sms_config['auth_token'])
        self.notifications: List[Dict[str, Any]] = []  # Store notifications for processing
        self.user_preferences: Dict[str, Dict[str, Any]] = {}  # User preferences for notifications

    def send_email(self, to: str, subject: str, message: str) -> None:
        """Send an email notification."""
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email_config['from_email']
            msg['To'] = to

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['from_email'], self.email_config['email_password'])
                server.sendmail(self.email_config['from_email'], to, msg.as_string())
            logging.info(f"Email sent to {to} with subject: {subject}")
        except Exception as e:
            logging.error(f"Failed to send email to {to}: {e}")

    def send_sms(self, to: str, message: str) -> None:
        """Send an SMS notification."""
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=self.sms_config['from_number'],
                to=to
            )
            logging.info(f"SMS sent to {to}: {message}")
        except Exception as e:
            logging.error(f"Failed to send SMS to {to}: {e}")

    async def notify_user(self, user_id: str, notification_type: str, message: str) -> None:
        """Notify a user via the specified notification type."""
        user_contact_info = self.get_user_contact_info(user_id)
        user_pref = self.user_preferences.get(user_id, {})

        if notification_type in user_pref.get('preferred_channels', []):
            if notification_type == 'email':
                self.send_email(user_contact_info['email'], "Notification", message)
            elif notification_type == 'sms':
                self.send_sms(user_contact_info['phone'], message)
            else:
                logging.warning(f"Unknown notification type: {notification_type}")
        else:
            logging.info(f"User  {user_id} has disabled {notification_type} notifications.")

    def get_user_contact_info(self, user_id: str) -> Dict[str, str]:
        """Mock function to get user contact information."""
        # In a real application, this would query a database or user management system
        return {
            'email': 'user@example.com',  # Replace with actual user email
            'phone': '+1234567890'        # Replace with actual user phone number
        }

    def queue_notification(self, user_id: str, notification_type: str, message: str) -> None:
        """Queue a notification for processing."""
        self.notifications.append({
            'user_id': user_id,
            'type': notification_type,
            'message': message
        })
        logging.info(f"Notification queued for user {user_id}: {message}")

    async def process_notifications(self) -> None:
        """Process all queued notifications asynchronously."""
        for notification in self.notifications:
            await self.notify_user(notification['user_id'], notification['type'], notification['message'])
        self.notifications.clear()  # Clear the queue after processing

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """Set user notification preferences."""
        self.user_preferences[user_id] = preferences
        logging.info(f"User  preferences updated for {user_id}: {preferences}")

    def render_template(self, template_str: str, context: Dict[str, Any]) -> str:
        """Render a notification template with context."""
        template = Template(template_str)
        return template.render(context)

# Example usage of the NotificationService class
if __name__ == "__main__":
    email_config = {
        'from_email': 'your_email@example.com',
        'email_password': 'your_email_password',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587
    }

    sms_config = {
        'account_sid': 'your_twilio_account_sid',
        'auth_token': 'your_twilio_auth_token',
        'from_number': '+1234567890'
    }

    notification_service = NotificationService(email_config, sms_config)

    # Set user preferences
    notification_service.set_user_preferences('user1', {
        'preferred_channels': ['email', 'sms']
    })

    # Queue a notification with a template
    message_template = "Hello {{ user_name }}, your transaction was successful!"
    message = notification_service.render_template(message_template, {'user_name': 'User 1'})
    notification_service.queue_notification('user1', 'email', message)
    notification_service.queue_notification('user1', 'sms', 'Your transaction was successful!')

    # Process notifications asynchronously
    asyncio.run(notification_service.process_notifications())
