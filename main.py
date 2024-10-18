from stream.multistream import MultiStream
from app.stream_app import StreamApp
import tkinter as tk
from tkinter import ttk



if __name__ == "__main__":
    # Create many stream 
    multi_stream = MultiStream()
    multi_stream.add_stream("Stream 1","udp://127.0.0.1:12345", "./video/loitering_people.webm")
    multi_stream.add_stream("Stream 2","udp://127.0.0.1:12346", "./video/loitering_people_extra.mp4")
    root = tk.Tk()# Assuming you have implemented MultiStream class
    app = StreamApp(root, "Stream Selection App", "1200x800", multi_stream)
    root.mainloop()

