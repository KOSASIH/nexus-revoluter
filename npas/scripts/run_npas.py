import time
import logging
from npas.core.synchronizer import NexusPiSynchronizer
from npas.utils.logger import setup_logger

def main():
    # Set up the logger for the main execution
    logger = setup_logger("MainExecution", level=logging.INFO, log_to_console=True)
    
    try:
        logger.info("Initializing NexusPiSynchronizer...")
        synchronizer = NexusPiSynchronizer()
        logger.info("NexusPiSynchronizer initialized successfully.")
        
        # Run the synchronizer in a loop with a specified interval
        interval = 60  # Run every 60 seconds
        logger.info(f"Starting synchronization loop with an interval of {interval} seconds.")
        
        while True:
            try:
                synchronizer.run(interval=interval)
                logger.info("Synchronization cycle completed successfully.")
            except Exception as e:
                logger.error(f"Error during synchronization cycle: {e}")
            
            time.sleep(interval)  # Wait for the specified interval before the next cycle

    except KeyboardInterrupt:
        logger.info("Synchronization process interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
    finally:
        logger.info("Shutting down NexusPiSynchronizer.")

if __name__ == "__main__":
    main()
