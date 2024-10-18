# main.py

import time
from detection.scheduler import Scheduler

def detection_task():
    print("Running detection task...")

# Initialize the job scheduler
scheduler = Scheduler()

# Start the scheduler
scheduler.start_scheduler()

# Add a new job to run the detection task every 5 seconds for 30 seconds
job_id = "detection_1"
interval = 5  # Run every 5 seconds
end_time = time.time() + 20  # Run for 30 seconds

scheduler.add_job(job_id, detection_task, interval, end_time)

# List all jobs
scheduler.list_jobs()

# Example: Delete the job after 15 seconds
time.sleep(30)
# scheduler.delete_job(job_id)
scheduler.list_jobs()
