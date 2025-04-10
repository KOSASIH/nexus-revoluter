# stress_test.py

import time
import threading
from holo_dashboard import HolographicGlobalDashboard

def stress_test_dashboard(dashboard):
    """Simulate high load on the dashboard."""
    for _ in range(100):  # Simulate 100 concurrent users
        threading.Thread(target=simulate_user_interaction, args=(dashboard,)).start()

if __name__ == "__main__":
    dashboard = HolographicGlobalDashboard()
    dashboard.start_dashboard()  # Start the dashboard
    start_time = time.time()
    stress_test_dashboard(dashboard)
    end_time = time.time()
    print(f"Stress test completed in {end_time - start_time:.2f} seconds.")
    dashboard.stop_dashboard()  # Stop the dashboard after testing
