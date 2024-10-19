import subprocess
from stream.multistream import MultiStream
import threading
import time
import cv2
import logging
import requests

logging.getLogger('opencv').setLevel(logging.ERROR)

class StreamController:
    def __init__(self):
        self.multi_stream = MultiStream()
        self.is_running = False
        self.processes = []  # List to keep track of streaming processes

    def start_streams(self):
        try:
            # Add streams
            self.multi_stream.add_stream("Stream 1", "udp://127.0.0.1:10001", "udp://127.0.0.1:10002", "./video/loitering_people.mp4")
            self.multi_stream.add_stream("Stream 2", "udp://127.0.0.1:10003", "udp://127.0.0.1:10004", "./video/loitering_people_extra.mp4")
            
            # Start all streams
            self.multi_stream.start_all_streams()
            self.is_running = True
            print("Streams started successfully.")
            return True
        except Exception as e:
            print(f"Error starting streams: {e}")
            return False

    def stop_streams(self):
        if self.is_running:
            self.multi_stream.stop_all_streams()
            self.is_running = False
            print("All streams have been stopped.")
        else:
            print("Streams are not currently running.")

def menu(controller):
    while True:
        print("\nStream Controller Menu:")
        print("1. Start Streams")
        print("2. Stop Streams")
        print("3. Checking streams")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            if not controller.is_running:
                result = controller.start_streams()
                continue
            else:
                print("Streams are already running.")
                continue
        elif choice == "2":
            controller.stop_streams()
            continue
        elif choice == "3":
            print("Number of online streams: ", len(controller.multi_stream.processes))
            controller.multi_stream.check_stream_status()
        elif choice == '4':
            controller.stop_streams()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    stream_controller = StreamController()
    # Start the menu in a separate thread to keep the main thread responsive
    menu_thread = threading.Thread(target=menu, args=(stream_controller,))
    menu_thread.start()

    try:
        # Keep the main thread alive
        while menu_thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping all streams due to KeyboardInterrupt...")
        stream_controller.stop_streams()
