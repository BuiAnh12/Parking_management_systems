from ultralytics import YOLO

class HumanDetection:
    def __init__(self):
        # Load the YOLOv8 model (using 'yolov8m' for medium accuracy and speed)
        self.model = YOLO('./model/yolov8m.pt')

    def detect(self, image):
        # Convert the image to the format required by YOLO
        results = self.model(image)

        # Initialize lists to hold bounding boxes and metadata
        bounding_boxes = []
        metadata = []

        # Process results
        for result in results:
            # Extract bounding box coordinates and confidence
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # bounding box coordinates (x1, y1, x2, y2)
                confidence = box.conf[0]       # confidence score
                label = int(box.cls[0])        # class index (0 for person)

                # Only keep detections for 'person' (class index 0)
                if label == 0:
                    bounding_boxes.append([x1.item(), y1.item(), x2.item() - x1.item(), y2.item() - y1.item()])
                    metadata.append({"label": "Person", "confidence": confidence.item()})

        return bounding_boxes, metadata
