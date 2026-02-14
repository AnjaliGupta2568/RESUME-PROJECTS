import cv2
import time
from ultralytics import YOLO
from utils.speed_estimation import SpeedEstimator
from utils.line_crossing import LineCrossingDetector


class TrafficSystem:

    def __init__(self, model_path="yolov8n.pt"):

        # Load YOLO model (auto downloads if not present)
        self.model = YOLO(model_path)

        # Speed & Line modules
        self.speed_estimator = SpeedEstimator()
        self.line_detector = LineCrossingDetector(line_y=400)

        self.vehicle_count = 0

        # COCO class IDs
        self.vehicle_classes = [2, 5, 7]  # Car, Bus, Truck

    # ------------------------------------------------
    # Process Single Frame
    # ------------------------------------------------
    def process_frame(self, frame):

        results = self.model(frame, verbose=False)
        detections = results[0].boxes

        for idx, box in enumerate(detections):

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls in self.vehicle_classes and conf > 0.5:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                object_id = idx

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Estimate Speed
                speed = self.speed_estimator.estimate_speed(
                    object_id, (center_x, center_y)
                )

                cv2.putText(frame,
                            f"Speed: {speed}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 0, 0),
                            2)

                # Check Line Crossing
                if self.line_detector.check_crossing(object_id, center_y):
                    self.vehicle_count += 1

        # Draw line
        cv2.line(frame,
                 (0, self.line_detector.line_y),
                 (frame.shape[1], self.line_detector.line_y),
                 (0, 0, 255),
                 2)

        return frame, self.vehicle_count

    # ------------------------------------------------
    # Process Video
    # ------------------------------------------------
    def process_video(self, video_path):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("❌ Error: Cannot open video file")
            return

        print("✅ Video Loaded Successfully")

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame, count = self.process_frame(frame)

            cv2.putText(frame,
                        f"Vehicle Count: {count}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        2)

            cv2.imshow("Intelligent Traffic AI System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("✅ Processing Finished")
