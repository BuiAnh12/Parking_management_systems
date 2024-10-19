import threading
import subprocess
import cv2
from stream.channel import Channel
import os

class MultiStream:
    def __init__(self):
        self.channel_manager = Channel()
        self.processes = []  # List to keep track of streaming processes
        self.threads = []  # List to keep track of threads

    def add_stream(self, name, display_channel_url, detect_channel_url, video_file):
        self.channel_manager.add_channel(name, display_channel_url, detect_channel_url, video_file)

    def start_all_streams(self):
        # Get all channels and start streaming them
        channels = self.channel_manager.get_channels()
        for channel in channels:
            # Start streaming in a separate thread for both display and detection
            display_thread = threading.Thread(target=self._start_streaming_process, args=(channel['name'], channel['video_file'], channel['display_channel_url']))
            detect_thread = threading.Thread(target=self._start_streaming_process, args=(channel['name'], channel['video_file'], channel['detect_channel_url']))
            display_thread.start()
            detect_thread.start()
            self.threads.extend([display_thread, detect_thread])

    def _start_streaming_process(self, name, input_video_path, udp_url):
        command = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', input_video_path,
            '-s', '640x360',
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-b:v', '500k',
            '-f', 'mpegts',
            '-loglevel', 'quiet',  # Suppress all logs
            '-threads', '1',
            udp_url
        ]

        # Run the command as a subprocess and redirect stdout and stderr to DEVNULL
        try:
            with open(os.devnull, 'w') as fnull:
                process = subprocess.Popen(command, stdout=fnull, stderr=fnull)
                self.processes.append({'name': name, 'url': udp_url, 'process': process})
        except Exception as e:
            print(f"An error occurred while starting the stream for {name}: {e}")

    def stop_all_streams(self):
        for process_info in self.processes:
            process_info['process'].terminate()
        self.processes = []
        print("All streams have been stopped.")

    def check_stream_status(self):
        # Check the status of all streaming processes
        status = []
        for process_info in self.processes:
            if process_info['process'].poll() is None:
                status.append((process_info['url'], "Running"))
            else:
                status.append((process_info['url'], "Stopped"))

        # Display the status
        for name, state in status:
            print(f"Stream {name}: {state}")

        return status
