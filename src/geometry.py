import cv2
import numpy as np

class TransformView:
    def __init__(self, area_points, warp_size, area_length):
        self.area = np.array(area_points, dtype=np.float32)
        w, h = warp_size
        dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
        self.matrix = cv2.getPerspectiveTransform(self.area, dst)
        self.meters_per_pixel = area_length / h

    def isIn(self, x, y):
        return cv2.pointPolygonTest(self.area, (float(x), float(y)), False) >= 0

    def transform_point(self, x, y):
        pts = np.array([[[x, y]]], dtype=np.float32)
        return cv2.perspectiveTransform(pts, self.matrix)[0][0]