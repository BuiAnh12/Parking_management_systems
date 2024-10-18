# job_scheduler.py

import schedule
import time
from threading import Thread

class Scheduler:
    def __init__(self):
        self.jobs = {}  # Dictionary to store jobs with unique job IDs

    def add_job(self, job_id, func, start_time, end_time, *args, **kwargs):
        """
        Add a new job to the scheduler to run once at the specified start time
        and loop until the end time or until the loop condition breaks.

        :param job_id: Unique ID for the job
        :param func: Function to be scheduled
        :param start_time: Time (in seconds since epoch) to start the job
        :param end_time: Time (in seconds since epoch) to stop the job
        :param args: Arguments for the function
        :param kwargs: Keyword arguments for the function
        """
        if job_id in self.jobs:
            print(f"Job with ID {job_id} already exists.")
            return

        # Define the job function with start and end time checks
        def job():
            current_time = time.time()
            if current_time >= start_time and current_time < end_time:
                if func(*args, **kwargs):
                    print(f"Job {job_id} completed successfully.")
                    print("Prepare to delete")
                    self.delete_job(job_id)  # Remove the job after execution
                    return
                else:
                    print(f"Job {job_id} is still running.")
            elif current_time >= end_time:
                print(f"Job {job_id} ended due to reaching end time.")
                self.delete_job(job_id)

        # Check if start time has already passed
        current_time = time.time()
        if current_time >= start_time:
            # Run the job immediately
            print(f"Job {job_id} is starting immediately as start time has passed.")
            self.jobs[job_id] = "executing"
            job()
        else:
            # Schedule the job to run at the specified start time
            delay = max(0, start_time - current_time)
            scheduled_job = schedule.every(delay).seconds.do(job)
            self.jobs[job_id] = scheduled_job
            print(f"Job {job_id} added successfully to run at {time.ctime(start_time)}.")

    
    def delete_job(self, job_id):
        if job_id in self.jobs:
            schedule.cancel_job(self.jobs[job_id])  # Cancel the scheduled job
            del self.jobs[job_id]  # Remove the job from the dictionary
            print(f"Job {job_id} has been deleted.")
        else:
            print(f"Job {job_id} not found.")


    def list_jobs(self):
        """List all active jobs."""
        if not self.jobs:
            print("No active jobs.")
            return None
        else:
            print("Active jobs:")
            for job_id, job in self.jobs.items():
                print(f"- Job ID: {job_id}, Next Run: {job.next_run}")
                return self.jobs.items()

    def run_pending(self):
        """Run all pending jobs."""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_scheduler(self):
        """Start the scheduler in a separate thread."""
        scheduler_thread = Thread(target=self.run_pending)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        print("Scheduler started.")
