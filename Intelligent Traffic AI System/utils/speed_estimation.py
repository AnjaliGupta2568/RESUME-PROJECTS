#speed_estimation

import time
import math

class SpeedEstimator:
    def __init__(self):
        self.previous_positions = {}
        self.previous_times = {}

    def estimate_speed(self, object_id, current_center):
        current_time = time.time()

        if object_id not in self.previous_positions:
            self.previous_positions[object_id] = current_center
            self.previous_times[object_id] = current_time
            return 0

        prev_center = self.previous_positions[object_id]
        prev_time = self.previous_times[object_id]

        distance = math.sqrt(
            (current_center[0] - prev_center[0])**2 +
            (current_center[1] - prev_center[1])**2
        )

        time_elapsed = current_time - prev_time

        speed = 0
        if time_elapsed > 0:
            speed = distance / time_elapsed

        self.previous_positions[object_id] = current_center
        self.previous_times[object_id] = current_time

        return round(speed, 2)
