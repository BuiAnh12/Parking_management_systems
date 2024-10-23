import time
import numpy as np
from ultralytics import YOLO

class LoiteringDetector:
    def __init__(self, loiter_time_threshold=10):
        """
        Initializes the LoiteringDetector.

        Args:
        model_path (str): Path to the YOLO model file.
        loiter_time_threshold (int): Time in seconds after which an object is considered loitering.
        """
        self.model = YOLO("./model/yolov8m.pt")
        self.loiter_time_threshold = loiter_time_threshold
        self.tracked_objects = {}  # Object ID -> {'start_time': timestamp, 'bbox': bbox}
        self.current_time = time.time()
        self.iou_threshold = 0.5  # Minimum IoU threshold to consider as the same object

    def detect(self, frame, confidence_threshold=0.5):
        """
        Detects loitering people and vehicles in the given video frame.

        Args:
        frame (np.array): The current video frame.
        confidence_threshold (float): Minimum confidence score for detections.

        Returns:
        bounding_boxes (list): List of bounding boxes for loitering objects or an empty list.
        metadata (list): List of metadata for loitering objects or an empty list.
        """        
        results = self.model(frame)
        bounding_boxes = []
        metadata = []

        self.current_time = time.time()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
                confidence = box.conf[0].item()  # Confidence score
                label = int(box.cls[0])  # Class index (0 for person)
                # Only keep detections for 'person' or vehicles (class indices: [0, 1, 2, 3, 5, 7])
                if label == 0 and confidence >= confidence_threshold:                    
                    object_id = self._track_object((x1, y1, x2, y2))
                    if object_id in self.tracked_objects:
                        start_time = self.tracked_objects[object_id]['start_time']
                        elapsed_time = self.current_time - start_time
                        if elapsed_time >= self.loiter_time_threshold:
                            print(f"[DEBUG] Object ID {object_id} is loitering. Bounding box: ({x1}, {y1}, {x2}, {y2}). Time: {elapsed_time:.2f}")
                            bounding_boxes.append([x1.item(), y1.item(), x2.item(), y2.item()])
                            metadata.append({"label": "Loitering Person", "confidence": confidence})

                    else:
                        # Start tracking a new object
                        print(f"[DEBUG] Starting to track new object ID: {object_id}")
                        self.tracked_objects[object_id] = {'start_time': self.current_time, 'bbox': (x1, y1, x2, y2)}

        # Clean up old tracked objects
        self._cleanup_old_objects()
        print(f"[DEBUG] Returning {len(bounding_boxes)} bounding boxes for loitering objects.")
        time.sleep(4)
        return bounding_boxes, metadata


    def _track_object(self, new_bbox):
        """
        Tracks an object based on IoU (Intersection over Union) with existing tracked objects.
        
        Args:
        new_bbox (tuple): Bounding box coordinates (x1, y1, x2, y2).

        Returns:
        object_id (int): The ID of the tracked object, or a new ID if not matched.
        """
        highest_iou = 0
        best_match_id = None

        for obj_id, data in self.tracked_objects.items():
            tracked_bbox = data['bbox']
            iou = self._calculate_iou(new_bbox, tracked_bbox)
            if iou > highest_iou and iou >= self.iou_threshold:
                highest_iou = iou
                best_match_id = obj_id

        if best_match_id is not None:
            # Update the tracked object with the new bbox
            self.tracked_objects[best_match_id]['bbox'] = new_bbox
            return best_match_id
        else:
            # Assign a new object ID if no match is found
            new_id = len(self.tracked_objects) + 1
            return new_id

    def _calculate_iou(self, box1, box2):
        """
        Calculates the Intersection over Union (IoU) of two bounding boxes.

        Args:
        box1 (tuple): Bounding box 1 (x1, y1, x2, y2).
        box2 (tuple): Bounding box 2 (x1, y1, x2, y2).

        Returns:
        float: IoU value between 0 and 1.
        """
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])

        # Compute intersection area
        inter_area = max(0, x2_inter - x1_inter + 1) * max(0, y2_inter - y1_inter + 1)

        # Compute areas of both bounding boxes
        box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

        # Compute union area
        union_area = box1_area + box2_area - inter_area

        # Compute IoU
        iou = inter_area / union_area if union_area > 0 else 0
        return iou

    def _cleanup_old_objects(self):
        """Removes tracked objects that have not been seen for a while."""
        current_time = time.time()
        objects_to_remove = [obj_id for obj_id, data in self.tracked_objects.items() 
                             if current_time - data['start_time'] > self.loiter_time_threshold * 2]

        for obj_id in objects_to_remove:
            del self.tracked_objects[obj_id]
