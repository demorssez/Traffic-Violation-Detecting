import numpy as np
from collections import deque
from src.geometry import TransformView


class SpeedEstimator:
    def __init__(self, transformer: TransformView, fps, window = 20):
        self.tf = transformer
        self.dt = 1 / fps
        self.window = window
        self.positions = {}
        self.speeds = {}

    def update(self, track_id, x, y):
        point = self.tf.transform_point(x, y)
        prev = self.positions.get(track_id)
        self.positions[track_id] = point
        if prev is None:
            return None

        distance = np.linalg.norm(point - prev) * self.tf.meters_per_pixel
        speed = distance / self.dt * 3.6
        buf = self.speeds.setdefault(track_id, deque(maxlen=self.window))
        buf.append(speed)
        return float(np.mean(buf))

    def n_samples(self, track_id):
        return len(self.speeds.get(track_id, ()))

    def reset(self, track_id: int):
        self.positions.pop(track_id, None)
        self.speeds.pop(track_id, None)
