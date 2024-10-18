import importlib
from threading import Thread
import cv2
import time 
from email_sender.sender import Sender
from detection.detection_type import car_detection, human_detection
class DetectionHandler:
    def __init__(self, detection_type, cap: cv2.VideoCapture):
        self.detection_type = detection_type
        self.cap = cap
        self.detector = self.load_detection_model()
        self.email_sender = Sender()


    def load_detection_model(self):
        if self.detection_type == 'human':
            return human_detection.HumanDetection()  # Create an instance
        elif self.detection_type == 'car':
            return car_detection.CarDetection()  # Create an instance
        return None

    def start_stream(self, stream_url):
        self.stop_flag = False
        if not self.cap.isOpened():
            print(f"Error: Unable to open stream {stream_url}")
            return
        print("Reading from stream " + stream_url)

    def run_detection(self, to_email):
        """Read frames from the stream at specified intervals and perform human detection."""
        try:
            while not self.stop_flag:
                # Read a frame from the stream
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame.")
                    continue  # Skip to the next iteration

                bounding_boxes, metadata = None, None
                if self.detector is not None and frame is not None:
                    bounding_boxes, metadata = self.detector.detect(frame)  
                else:
                    print("Detection model not available.")

                if bounding_boxes:
                    # Get the frame with bounding boxes
                    frame_with_boxes = self.draw_bounding_boxes(frame, bounding_boxes, metadata) 

                    # Generate image save path 
                    img_id = str(time.time())[:5]
                    img_path = f"output/detected_frame_{self.detection_type}_{img_id}.jpg"  

                    # Save the frame 
                    cv2.imwrite(img_path, frame_with_boxes)

                    # Send email and end the process
                    self.email_sender.send_custom_email(to_email, self.detection_type, img_path)
                    return True

                # Sleep for the specified interval
                time.sleep(1)

        except Exception as e:
            print(f'Fail to run detection: {e}')

            

    def stop_reading_stream(self):
        """Stop the video stream."""
        self.stop_flag = True
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def join_thread(self):
        """Join the stream thread if needed."""
        if self.stream_thread is not None:
            self.stream_thread.join()
    

    @staticmethod
    def draw_bounding_boxes(image, bounding_boxes, metadata):
        for i, box in enumerate(bounding_boxes):
            x, y, w, h = box
            label = metadata[i].get("label", "Object")
            confidence = metadata[i].get("confidence", 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image

    @staticmethod
    def save_image(image, output_path):
        cv2.imwrite(output_path, image)
        print(f"Image saved to {output_path}")
