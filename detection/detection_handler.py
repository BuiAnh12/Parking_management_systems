import importlib
from threading import Thread
import cv2
import time 
from email_sender.sender import Sender
from detection.detection_type import car_detection, human_detection
class DetectionHandler:
    def __init__(self, detection_type, stream_app):
        self.detection_type = detection_type
        self.stream_app = stream_app
        self.detector = self.load_detection_model()
        self.email_sender = Sender()
        self.stop_flag = False


    def load_detection_model(self):
        if self.detection_type == 'human':
            return human_detection.HumanDetection()  # Create an instance
        elif self.detection_type == 'car':
            return car_detection.CarDetection()  # Create an instance
        return None

    def run_detection(self, to_email):
        """Read frames from the stream at specified intervals and perform human detection."""
        try:
            while not self.stop_flag:
                # Read a frame from the stream
                if not self.stream_app.frame_queue.empty():
                    frame =  self.stream_app.frame_queue.get()

                bounding_boxes, metadata = None, None
                if self.detector is not None and frame is not None:
                    bounding_boxes, metadata = self.detector.detect(frame, 0.75)  
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


    def join_thread(self):
        """Join the stream thread if needed."""
        if self.stream_thread is not None:
            self.stream_thread.join()
    

    @staticmethod
    def draw_bounding_boxes(image, bounding_boxes, metadata):
        for i, box in enumerate(bounding_boxes):
            x1, y1, x2, y2 = box  # Unpack the bounding box coordinates
            label = metadata[i].get("label", "Object")
            confidence = metadata[i].get("confidence", 0)

            # Draw the rectangle using the coordinates
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # # Prepare the label text
            # text = f"{label}: {confidence:.2f}"

            # # # Draw the label text above the bounding box
            # # cv2.putText(image, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image

    @staticmethod
    def save_image(image, output_path):
        cv2.imwrite(output_path, image)
        print(f"Image saved to {output_path}")
