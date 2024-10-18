import cv2

def main():
    # URL or camera index for video capture
    # Replace '0' with the URL of your video stream or IP camera
    # For example: 'http://192.168.1.2:8080/video' for an IP camera
    stream_source = "udp://127.0.0.1:12346"  # '0' is typically the default webcam; change as needed

    # Create a VideoCapture object
    cap = cv2.VideoCapture(stream_source)

    # Check if the video capture is successfully opened
    if not cap.isOpened():
        print("Error: Could not open the video stream.")
        return

    # Loop to continuously get frames
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret will be True
        if not ret:
            print("Error: Cannot read frame from the stream.")
            break

        # Display the resulting frame
        cv2.imshow('Video Stream', frame)

        # Press 'q' to exit the loop and close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
