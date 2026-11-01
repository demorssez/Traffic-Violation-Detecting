class OffenderRegistry:
    def __init__(self, min_samples = 10):
        self.min_samples = min_samples
        self.max_speed = {}
        self.shots = set()

    def upd(self, track_id, speed):
        self.max_speed[track_id] = max(speed, self.max_speed.get(track_id, 0.0))

    def to_be_offender(self, track_id, n_samples):
        return track_id not in self.shots and n_samples >= self.min_samples

    def set_offender(self, track_id):
        self.shots.add(track_id)