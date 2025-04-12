import logging
import functools
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ErrorHandler:
    def __init__(self, logger, email_notifications=False, email_config=None):
        self.logger = logger
        self.email_notifications = email_notifications
        self.email_config = email_config

    def send_email(self, subject, message):
        if not self.email_config:
            self.logger.warning("Email configuration not provided. Skipping email notification.")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['from'], self.email_config['password'])
                server.send_message(msg)

            self.logger.info("Error notification email sent successfully.")
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")

    def handle_error(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"An error occurred in {func.__name__}: {e}")
                if self.email_notifications:
                    self.send_email(
                        subject=f"Critical Error in {func.__name__}",
                        message=f"An error occurred: {e}\n\nFunction: {func.__name__}\nArguments: {args}, {kwargs}"
                    )
                raise  # Re-raise the exception after logging
        return wrapper

# Example usage
if __name__ == "__main__":
    from utils.logger import CustomLogger

    logger = CustomLogger(__name__)
    email_config = {
        'from': 'your_email@example.com',
        'to': 'admin@example.com',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'password': 'your_email_password'
    }

    error_handler = ErrorHandler(logger, email_notifications=True, email_config=email_config)

    @error_handler.handle_error
    def risky_function(x):
        return 10 / x  # This will raise an exception if x is 0

    # Test the error handling
    try:
        risky_function(0)
    except ZeroDivisionError:
        logger.info("Handled division by zero error.")
