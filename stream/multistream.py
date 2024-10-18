import threading
import subprocess
from stream.channel import Channel
import datetime
class MultiStream:
    def __init__(self):
        self.channel_manager = Channel()
        self.processes = []  # List to keep track of streaming processes

    def add_stream(self, name, channel_url, video_file):
        self.channel_manager.add_channel(name, channel_url, video_file)

    def start_all_streams(self):
        # Get all channels and start streaming them
        channels = self.channel_manager.get_channels()
        for channel in channels:
            # Start streaming in a separate thread
            thread = threading.Thread(target=self._start_streaming_process, args=(channel['video_file'], channel['channel_url']))
            thread.start()

    def _start_streaming_process(self, input_video_path, udp_url):
        # Use FFmpeg to stream the video using UDP
        command = [
            'ffmpeg',
            '-stream_loop', '-1',  # Loop the input video infinitely
            '-re',  # Read input video in real-time
            '-i', input_video_path,  # Input file path
            '-c:v', 'libx264',  # Encode video with H.264 codec
            '-preset', 'ultrafast',  # Use the ultrafast preset for streaming
            '-fflags', 'nobuffer',  # Disable buffering
            '-flags', 'low_delay',  # Low delay
            '-f', 'mpegts',  # Format for streaming
            '-loglevel', 'quiet',  # Suppress all logs
            '-threads', '1',  # Use a single thread for decoding
            udp_url  # UDP URL
        ]


        # Run the command as a subprocess and redirect stdout and stderr to DEVNULL
        try:
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.processes.append(process)
        except Exception as e:
            print(f"An error occurred while starting the stream: {e}")

    def stop_all_streams(self):
        for process in self.processes:
            process.terminate()
        self.processes = []
        print("All streams have been stopped.")

    def check_stream_status(self):
        # Check the status of all streaming processes
        status = []
        for idx, process in enumerate(self.processes):
            if process.poll() is None:
                status.append((idx, "Running"))
            else:
                status.append((idx, "Stopped"))

        # Display the status
        for idx, state in status:
            print(f"Stream {idx}: {state}")

        # Optionally, return the status list for further processing
        return status
