import time
import logging
from collections import defaultdict
from threading import Lock

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(int)  # Store counts of metrics
        self.timing_metrics = defaultdict(list)  # Store timing metrics
        self.lock = Lock()  # Ensure thread safety
        self.logger = logging.getLogger("MetricsCollector")
        self.logger.setLevel(logging.INFO)

    def record(self, metric_name, value=1):
        """Record a metric count."""
        with self.lock:
            self.metrics[metric_name] += value
            self.logger.info(f"Metric recorded: {metric_name} = {self.metrics[metric_name]}")

    def record_timing(self, metric_name, duration):
        """Record timing for a specific metric."""
        with self.lock:
            self.timing_metrics[metric_name].append(duration)
            self.logger.info(f"Timing recorded: {metric_name} = {duration:.2f} seconds")

    def report(self):
        """Generate a report of collected metrics."""
        with self.lock:
            report_lines = ["--- Metrics Report ---"]
            for metric, count in self.metrics.items():
                report_lines.append(f"{metric}: {count}")
            for metric, timings in self.timing_metrics.items():
                avg_time = sum(timings) / len(timings) if timings else 0
                report_lines.append(f"{metric} (avg time): {avg_time:.2f} seconds over {len(timings)} records")
            report = "\n".join(report_lines)
            self.logger.info(report)
            return report

    def reset(self):
        """Reset all collected metrics."""
        with self.lock:
            self.metrics.clear()
            self.timing_metrics.clear()
            self.logger.info("Metrics have been reset.")

    def log_metrics_to_file(self, file_path):
        """Log metrics to a specified file."""
        with open(file_path, 'a') as f:
            f.write(self.report() + "\n")

    def log_metrics_to_console(self):
        """Log metrics to the console."""
        print(self.report())

# Example usage
if __name__ == "__main__":
    collector = MetricsCollector()
    collector.record("api_calls")
    collector.record_timing("api_call_duration", 0.123)
    collector.record("api_calls", 2)  # Increment by 2
    collector.report()
