# job_scheduler.py

import schedule
import time
from threading import Thread, Timer

class Scheduler:
    def __init__(self):
        self.jobs = {}  # Dictionary to store jobs with unique job IDs

    def add_job(self, job_id, func, start_time, *args, **kwargs):
        if job_id in self.jobs:
            print(f"Job with ID {job_id} already exists.")
            return

        # Define the job function
        def job():
            print("Job activated")
            result = func(*args, **kwargs)
            if result:
                print(f"Job {job_id} completed successfully.")
            else:
                print(f"Job {job_id} encountered a problem")
            # Automatically delete the job after it runs
            self.delete_job(job_id)

        # Define a function to stop the job
        def stop_job():
            print(f"Job {job_id} is stopping due to reaching the end time.")
            self.delete_job(job_id)

        current_time = time.time()
        start_delay = max(0, start_time - current_time)
        start_timer = Timer(start_delay, job)
        start_timer.start()

        self.jobs[job_id] = start_timer
        print(f"Job {job_id} added to run at {time.ctime(start_time)}")

    def delete_job(self, job_id):
        if job_id in self.jobs:
            start_timer = self.jobs[job_id]
            start_timer.cancel()  # Cancel the start timer
            del self.jobs[job_id]
            print(f"Job {job_id} has been deleted.")
        else:
            print(f"Job {job_id} not found.")


