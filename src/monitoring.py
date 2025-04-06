import logging
import time
import psutil
import json
from datetime import datetime
from typing import Dict, Any

class Monitoring:
    def __init__(self, log_file: str = "system_monitor.log"):
        """Initialize the monitoring system with logging configuration."""
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Monitoring system initialized.")

    def log_system_metrics(self):
        """Log system metrics such as CPU, memory, and disk usage."""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        metrics = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_info.percent,
            "memory_total": memory_info.total,
            "memory_available": memory_info.available,
            "disk_usage": disk_info.percent,
            "disk_total": disk_info.total,
            "disk_used": disk_info.used,
            "disk_free": disk_info.free,
            "timestamp": datetime.now().isoformat()
        }

        logging.info("System Metrics: %s", json.dumps(metrics))
        return metrics

    def log_transaction(self, transaction_id: str, status: str, details: Dict[str, Any]):
        """Log transaction details."""
        log_entry = {
            "transaction_id": transaction_id,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        logging.info("Transaction Log: %s", json.dumps(log_entry))

    def log_error(self, error_message: str):
        """Log error messages."""
        logging.error("Error: %s", error_message)

    def log_event(self, event_message: str):
        """Log general events."""
        logging.info("Event: %s", event_message)

    def monitor(self, interval: int = 60):
        """Continuously monitor system metrics at a specified interval."""
        try:
            while True:
                self.log_system_metrics()
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user.")

# Example usage
if __name__ == "__main__":
    monitoring = Monitoring()

    # Start monitoring in a separate thread or process in a real application
    try:
        monitoring.monitor(interval=10)  # Log metrics every 10 seconds
    except Exception as e:
        monitoring.log_error(str(e))
