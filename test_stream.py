import cv2

def main():
    stream_source = "udp://127.0.0.1:10004"  # RTSP stream URL

    # Create a VideoCapture object
    cap = cv2.VideoCapture(stream_source)

    if not cap.isOpened():
        print("Error: Could not open the video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame from the stream.")
            break
        
        cv2.imshow('Video Stream', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
