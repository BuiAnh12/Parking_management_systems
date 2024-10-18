from detection.detection_type.human_detection import HumanDetection
import cv2

def main():
    # Initialize the HumanDetection class
    detector = HumanDetection()

    # Open a video capture object (0 for the default webcam, or replace with a video file path)
    cap = cv2.VideoCapture("udp://127.0.0.1:12346")  # Use '0' for webcam or replace with 'path/to/video.mp4'

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        # Perform detection
        boxes, metadata = detector.detect(frame)

        # Draw bounding boxes on the frame
        for box in boxes:
            x, y, w, h = box
            cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)

        # Display the frame with detections
        cv2.imshow("Human Detection", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()