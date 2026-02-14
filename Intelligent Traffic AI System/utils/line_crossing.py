# line_crossing

class LineCrossingDetector:
    def __init__(self, line_y=400):
        self.line_y = line_y
        self.crossed_ids = set()

    def check_crossing(self, object_id, center_y):
        if center_y > self.line_y and object_id not in self.crossed_ids:
            self.crossed_ids.add(object_id)
            return True
        return False
