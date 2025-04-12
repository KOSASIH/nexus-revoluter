import logging
import smtplib
from email.mime.text import MIMEText
from functools import wraps

# Custom Exception Classes
class ApiError(Exception):
    """Base class for API-related errors."""
    pass

class ConnectionError(ApiError):
    """Exception raised for connection errors."""
    pass

class TimeoutError(ApiError):
    """Exception raised for timeout errors."""
    pass

class HttpError(ApiError):
    """Exception raised for HTTP errors."""
    def __init__(self, response):
        self.response = response
        super().__init__(f"HTTP Error: {response.status_code} - {response.text}")

# Setup logger
logger = logging.getLogger("ErrorHandler")
logger.setLevel(logging.ERROR)

# Email notification settings (optional)
EMAIL_NOTIFICATIONS_ENABLED = True
EMAIL_SENDER = "your_email@example.com"
EMAIL_RECEIVER = "developer@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@example.com"
SMTP_PASSWORD = "your_email_password"

def send_error_notification(error_message):
    """Send an email notification about an error."""
    if EMAIL_NOTIFICATIONS_ENABLED:
        msg = MIMEText(error_message)
        msg['Subject'] = 'Critical Error Notification'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            logger.info("Error notification sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")

def handle_api_error(exception, logger):
    """Handle API errors and log them appropriately."""
    if isinstance(exception, ConnectionError):
        logger.error("Connection error occurred.")
        send_error_notification("Connection error occurred.")
    elif isinstance(exception, TimeoutError):
        logger.error("Request timed out.")
        send_error_notification("Request timed out.")
    elif isinstance(exception, HttpError):
        logger.error(f"HTTP error occurred: {exception.response.status_code} - {exception.response.text}")
        send_error_notification(f"HTTP error occurred: {exception.response.status_code} - {exception.response.text}")
    else:
        logger.error(f"An unexpected error occurred: {exception}")
        send_error_notification(f"An unexpected error occurred: {exception}")

def retry_on_exception(max_retries=3, delay=2):
    """Decorator to retry a function on exception."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        logger.error(f"All attempts failed for {func.__name__}: {e}")
                        raise
        return wrapper
    return decorator
