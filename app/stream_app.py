import tkinter as tk
from tkinter import ttk
import cv2
from threading import Lock, Thread
from PIL import Image, ImageTk
from time import sleep, time
from queue import Queue
from datetime import datetime
from tkcalendar import DateEntry
from detection.scheduler import Scheduler
from detection.detection_handler import DetectionHandler
import sys
import os
import cv2
from contextlib import redirect_stderr



# Define a dictionary for detection type mapping
detection_mapping = {
    "Detect People": "human",
    "Detect Vehicle": "car",
}


class StreamApp:
    def __init__(self, root, title, geometry, multistream):
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)

        # Initialize MultiStream
        self.multi_stream = multistream

        # Initialise Scheduler
        self.scheduler = Scheduler()

        # Selected stream variable
        self.selected_stream = None
        self.cap = None
        self.stop_flag = False  # Control flag for stopping the stream
        self.frame_queue = Queue(maxsize=10)  # A queue to hold frames
        # Set up the UI
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mutex = Lock()
        cv2.setLogLevel(0)
        print(cv2.getLogLevel())


    def setup_ui(self):
        # Left frame for stream selection
        self.left_frame = tk.Frame(self.root, width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_frame.pack_propagate(False)

        # Right frame for video display
        self.right_frame = tk.Frame(self.root, bg="black")
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Canvas for displaying the video stream
        self.video_canvas = tk.Canvas(self.right_frame, bg="black")
        self.video_canvas.pack(expand=True, fill=tk.BOTH)

        # Stream list
        self.stream_list = tk.Listbox(self.left_frame)
        self.stream_list.pack(fill=tk.BOTH, expand=True)
        self.stream_list.bind("<<ListboxSelect>>", self.switch_stream)

        # Frame for task selection
        self.task_frame = tk.Frame(self.left_frame)
        self.task_frame.pack(fill=tk.X, pady=10)

        # Label for task selection
        self.task_label = tk.Label(self.task_frame, text="Select Mission")
        self.task_label.pack(anchor=tk.W, padx=5)

        # Dropdown for task selection (using Combobox as a placeholder)
        self.task_options = ["Detect People", "Detect Vehicle", "Other Mission 1", "Other Mission 2"]
        self.task_combobox = ttk.Combobox(self.task_frame, values=self.task_options)
        self.task_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.task_combobox.current(0)  # Set the default selection
        self.task_combobox.bind("<<ComboboxSelected>>", self.on_task_selected)

        # Frame for user inputs (start time, end time, email)
        self.user_input_frame = tk.Frame(self.left_frame)
        self.user_input_frame.pack(fill=tk.X, pady=10)

        # Start time input
        self.start_time_label = tk.Label(self.user_input_frame, text="Start Time")
        self.start_time_label.pack(anchor=tk.W, padx=5)

        # Date picker for start time
        self.start_date_entry = DateEntry(self.user_input_frame, width=18)
        self.start_date_entry.pack(fill=tk.X, padx=5, pady=5)

        # Time selection for start time
        self.start_time_options = [f"{hour:02d}:00" for hour in range(24)]
        self.start_time_combobox = ttk.Combobox(self.user_input_frame, values=self.start_time_options)
        self.start_time_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.start_time_combobox.current(0)

        # End time input
        self.end_time_label = tk.Label(self.user_input_frame, text="End Time")
        self.end_time_label.pack(anchor=tk.W, padx=5)

        # Date picker for end time
        self.end_date_entry = DateEntry(self.user_input_frame, width=18)
        self.end_date_entry.pack(fill=tk.X, padx=5, pady=5)

        # Time selection for end time
        self.end_time_combobox = ttk.Combobox(self.user_input_frame, values=self.start_time_options)
        self.end_time_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.end_time_combobox.current(0)

        # Email input
        self.email_label = tk.Label(self.user_input_frame, text="Email")
        self.email_label.pack(anchor=tk.W, padx=5)
        self.email_entry = tk.Entry(self.user_input_frame)
        self.email_entry.pack(fill=tk.X, padx=5, pady=5)
        self.email_entry.insert(0, "buianh120403@gmail.com")

        # Button to add task to upcoming tasks
        self.add_task_button = tk.Button(self.user_input_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(fill=tk.X, padx=5, pady=10)

        # Frame for upcoming tasks
        self.upcoming_tasks_frame = tk.Frame(self.left_frame)
        self.upcoming_tasks_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Label for upcoming tasks
        self.upcoming_tasks_label = tk.Label(self.upcoming_tasks_frame, text="Upcoming Tasks")
        self.upcoming_tasks_label.pack(anchor=tk.W, padx=5)

        # Listbox for upcoming tasks
        self.upcoming_tasks_listbox = tk.Listbox(self.upcoming_tasks_frame)
        self.upcoming_tasks_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Load the stream list
        self.load_stream_list()

    def load_stream_list(self):
        # Populate the stream list with channel URLs
        channels = self.multi_stream.channel_manager.get_channels()
        print(channels)
        for channel in channels:
            self.stream_list.insert(tk.END, channel['name'])
        

    def start_stream(self):
        # Get the selected stream from the list
        selected_index = self.stream_list.curselection()
        if not selected_index:
            print("No stream selected")
            return

        # Get the channel URL from the selected item
        selected_channel_name = self.stream_list.get(selected_index[0])
        channels = self.multi_stream.channel_manager.get_channels()
        self.selected_display_channel_url = None
        for channel in channels:
            if channel.get('name') == selected_channel_name:
                self.selected_display_channel_url = channel.get('display_channel_url')
                self.selected_detect_channel_url = channel.get('detect_channel_url')
        print(self.selected_display_channel_url)
        print(self.selected_detect_channel_url)
        # If a stream is already running, stop it first
        
        self.stream_thread = Thread(target=self.update_frame)
        self.stream_thread.daemon = True  # Daemonize the thread
        self.stream_thread.start()

    def switch_stream(self, event):
        # Switch to a new stream based on the selected item in the list
        self.start_stream()
        

    def on_task_selected(self, event):
        # Determine the selected task
        selected_task = self.task_combobox.get()
        print(f"Selected task: {selected_task}")
        # Here you can add additional logic to handle the selected task

    def add_task(self):
        # Get user input values
        selected_task = self.task_combobox.get()
        start_date = self.start_date_entry.get()
        start_time = self.start_time_combobox.get()
        end_date = self.end_date_entry.get()
        end_time = self.end_time_combobox.get()
        email = self.email_entry.get()
        display_stream = self.selected_display_channel_url
        detect_stream = self.selected_detect_channel_url

        start_timestamp = self.convert_to_timestamp(start_date, start_time)
        end_timestamp = self.convert_to_timestamp(end_date, end_time)
        print(start_timestamp)
        print(end_timestamp)

        # Format the task details
        task_details = f"{selected_task} | Start: {start_date} {start_time} | End: {end_date} {end_time} | Email: {email} | Stream: {display_stream}"

        # Add the task to the upcoming tasks list
        self.upcoming_tasks_listbox.insert(tk.END, task_details)
        print(f"Added task: {task_details}")

        # Create schedule for that task in a separate thread
        task_id = f'{detection_mapping[selected_task]}_{str(time())}'
        thread = Thread(target=self.activate_detection, args=(selected_task, task_id, email, start_timestamp, end_timestamp, detect_stream))
        thread.start()

    def activate_detection(self, selected_task, task_id, email, start_timestamp, end_timestamp, stream_url):
        # This activates the detection flow without pausing the app by using a thread

        # Initialize Detection Handler
        self.detection_handler = DetectionHandler(detection_mapping[selected_task], self)
        # Add the detection job to the scheduler
        self.scheduler.add_job(task_id, self.detection_handler.run_detection, start_timestamp, email, stream_url, end_timestamp)


        print(f"Detection activated for task: {task_id}")


    def update_frame(self):
        with open(os.devnull, 'w') as fnull, redirect_stderr(fnull):
            try:
                if self.cap:
                    self.stop_stream()
                    self.stream_thread = None
                # Set the stop flag to False and start a new thread to read the stream
                self.stop_flag = False
                self.cap = cv2.VideoCapture(self.selected_display_channel_url)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                print("Start cap")
                sleep(1)
                print("Start read")
                self.mutex.acquire()
                retry = 3
                while not self.stop_flag:
                    if retry <= 0: 
                        print("Out of retry")
                        self.cap.release()
                        return 
                    
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    ret, frame = self.cap.read()
                    if not ret:
                        print("Error: Unable to read frame from the stream.")
                        sleep(0.1)
                        retry -= 1
                        continue

                    # Get the current timestamp
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Overlay the timestamp on the frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, current_time, (10, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                    # Convert the frame to RGB (Tkinter uses RGB)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame_rgb)
                    image_tk = ImageTk.PhotoImage(image=image)

                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                    else:
                        self.frame_queue.get()
                        self.frame_queue.put(frame)

                    
                    # Update the Canvas with the new frame in a thread-safe manner
                    self.video_canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
                    self.video_canvas.image = image_tk
                    self.root.update_idletasks()


                # Release the capture once the loop is over
                self.cap.release()
            except Exception as e:
                print(f"Error occurred: {e}")
                self.cap.release()
            finally:
                self.mutex.release()

    def stop_stream(self):
        # Stop the current stream
        self.stop_flag = True  # Set the stop flag to True to stop the streaming loop
        if self.cap:
            self.cap.release()
        self.cap = None

    def on_close(self):
        # Stop all running streams
        self.stop_stream()
        # Destroy the Tkinter window
        self.root.destroy()

    def convert_to_timestamp(self, date, time):
        """
        Convert start and end date/time strings to Unix timestamps.

        :param date: Start date in the format 'YYYY-MM-DD'
        :param time: Start time in the format 'HH:MM'
        :return: timestamp
        """
        # Combine date and time into single strings
        datetime_str = f"{date} {time}"


        # Define the format
        datetime_format = '%m/%d/%y %H:%M'

        # Convert to datetime objects
        datetime_object = datetime.strptime(datetime_str, datetime_format)

        # Convert to Unix timestamps
        timestamp = int(datetime_object.timestamp())

        return timestamp
