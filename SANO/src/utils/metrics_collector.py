import time
import psutil
import logging
import functools

class MetricsCollector:
    def __init__(self, logger):
        self.logger = logger

    def log_metrics(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss  # Resident Set Size

            result = func(*args, **kwargs)

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss

            execution_time = end_time - start_time
            memory_used = end_memory - start_memory

            self.logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds, "
                             f"memory used: {memory_used / (1024 * 1024):.2f} MB")

            return result
        return wrapper

# Example usage
if __name__ == "__main__":
    from utils.logger import CustomLogger

    logger = CustomLogger(__name__)
    metrics_collector = MetricsCollector(logger)

    @metrics_collector.log_metrics
    def sample_function(n):
        """A sample function that simulates some work."""
        total = 0
        for i in range(n):
            total += i ** 2
        return total

    # Test the metrics collector
    result = sample_function(1000000)
    logger.info(f"Result of sample_function: {result}")
