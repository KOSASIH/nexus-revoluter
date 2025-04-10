import time
import threading
from holo_dashboard import HolographicGlobalDashboard

def simulate_user_interaction(dashboard):
    """Simulate user interactions with the dashboard."""
    for _ in range(10):  # Simulate 10 interactions per thread
        command = "Show transactions"  # Example command
        response = dashboard.user_experience.process_voice_command(command)
        print(response)  # Print the response for monitoring
        time.sleep(0.1)  # Simulate a slight delay between commands

def stress_test_dashboard(dashboard):
    """Simulate high load on the dashboard."""
    threads = []
    for _ in range(100):  # Simulate 100 concurrent users
        thread = threading.Thread(target=simulate_user_interaction, args=(dashboard,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    dashboard = HolographicGlobalDashboard()
    dashboard.start_dashboard()  # Start the dashboard
    start_time = time.time()
    
    stress_test_dashboard(dashboard)  # Perform the stress test
    
    end_time = time.time()
    print(f"Stress test completed in {end_time - start_time:.2f} seconds.")
    
    dashboard.stop_dashboard()  # Stop the dashboard after testing
