# performance_test.py

import time
import random

def simulate_user_interaction(dashboard):
    """Simulate user interactions with the dashboard."""
    for _ in range(100):  # Simulate 100 interactions
        command = random.choice(["Show transactions", "Show nodes", "Show liquidity"])
        dashboard.user_experience.process_voice_command(command)
        time.sleep(0.1)  # Simulate a slight delay between commands

if __name__ == "__main__":
    from holo_dashboard import HolographicGlobalDashboard
    dashboard = HolographicGlobalDashboard()
    start_time = time.time()
    simulate_user_interaction(dashboard)
    end_time = time.time()
    print(f"Performance test completed in {end_time - start_time:.2f} seconds.")
