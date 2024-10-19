# test_scheduler.py

import time
from detection.scheduler import Scheduler

def test_function(message):
    """A simple function to be scheduled that prints a message."""
    print(message)
    while True:
        print("still going")
        time.sleep(1)
    # Return True to indicate successful execution

if __name__ == "__main__":
    # Create a Scheduler instance
    scheduler = Scheduler()

    # Get the current time
    current_time = time.time()

    # Set the start time to 30 seconds from now
    start_time = current_time + 5
    # Set the end time to 60 seconds from now
    end_time = current_time + 10

    # Add a job to the scheduler
    scheduler.add_job(
        job_id="test_job",
        func=test_function,
        start_time=start_time,
        end_time=end_time,
        message="This is a test message running after 30 seconds."
    )

    # Keep the main thread running to allow the scheduler to execute jobs
    while True:
        time.sleep(1)
        
