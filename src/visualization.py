import cv2
import numpy as np

GREEN = (0, 255, 0)
RED = (0, 0, 255)
GRAY = (128, 128, 128)


def draw_box(frame, box, color, label=None):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    if label:
        cv2.putText(frame, label, (x1 + 10, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


def put_text_scaled(frame, text, pos, width_ratio, color, thickness=2):
    w = frame.shape[1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, _), _ = cv2.getTextSize(text, font, 1.0, thickness)
    scale = w * width_ratio / text_w
    cv2.putText(frame, text, pos, font, scale, color, thickness, cv2.LINE_AA)


def crop_box(frame, box, pad_x=0, pad_y=0):
    h, w = frame.shape[:2]
    x1, y1, x2, y2 = box
    return frame[max(0, y1 - pad_y):min(h, y2 + pad_y), max(0, x1 - pad_x):min(w, x2 + pad_x)].copy()


def build_evidence(clean_frame, box, plate, speed, limit):
    shot = crop_box(clean_frame, box, pad_x=240, pad_y=120)
    h, w = shot.shape[:2]
    text = f'License plate: {plate}    Speed: {speed:.1f} km/h (Limit: {limit} km/h)'
    cv2.rectangle(shot, (0, h - 40), (w, h), (0, 0, 0), cv2.FILLED)
    put_text_scaled(shot, text, (10, h - 15), 0.8, (255, 255, 255))
    return shot
