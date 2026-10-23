import time
import cv2
from pathlib import Path
from ultralytics import YOLO
from src.config import Config
from src.geometry import TransformView
from src.offenders import OffenderRegistry
from src.plate_number import read_plate
from src.speed import SpeedEstimator
from src.visualization import GRAY, GREEN, RED, build_evidence, crop_box, draw_box


class Pipeline:
    def __init__(self, cfg, show = True):
        self.cfg = cfg
        self.show = show
        self.model = YOLO(cfg.model_path)
        self.tf = TransformView(cfg.area_points, cfg.warp_size, cfg.area_length)
        self.registry = OffenderRegistry(cfg.min_samples)
        self.windows = {}

    def run(self):
        start = time.time()
        cfg = self.cfg

        cap = cv2.VideoCapture(cfg.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        Path(cfg.output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(cfg.offenders).mkdir(parents=True, exist_ok=True)
        out = cv2.VideoWriter(cfg.output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        self.speed = SpeedEstimator(self.tf, fps, cfg.speed_window)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            clean = frame.copy()
            result = self.model.track(
                frame, tracker=cfg.track_path, persist=True, verbose=False)[0]
            self._process(frame, clean, result)

            out.write(frame)
            if self.show:
                cv2.imshow('Main', frame)
                for tid, shot in self.windows.items():
                    cv2.imshow(f'Offender {tid}', shot)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        end = round(time.time() - start, 1)
        print(f'Execution time: {int(end // 60)}:{int(end % 60):02d} min')

    def _process(self, frame, clean, result):
        boxes = result.boxes
        if boxes is None or boxes.id is None:
            return

        for box, id in zip(boxes.xyxy.int().tolist(), boxes.id.int().tolist()):
            x1, y1, x2, y2 = box
            cx, cy = (x1 + x2) / 2, y2

            if not self.tf.isIn(cx, cy):
                self.speed.reset(id)
                draw_box(frame, box, GRAY)
                continue

            speed = self.speed.update(id, cx, cy)
            if speed is None:
                draw_box(frame, box, GREEN, '...')
                continue

            label = f'Speed: {speed:.1f} km/h'
            if speed >= self.cfg.speed_limit:
                draw_box(frame, box, RED, label)
                self.registry.upd(id, speed)
                if self.registry.to_be_offender(id, self.speed.n_samples(id)):
                    self._capture(clean, box, id)
            else:
                draw_box(frame, box, GREEN, label)

    def _capture(self, clean, box, id):
        plate = read_plate(crop_box(clean, box))
        speed = self.registry.max_speed[id]
        shot = build_evidence(clean, box, plate, speed, self.cfg.speed_limit)

        self.windows[id] = shot
        cv2.imwrite(str(Path(self.cfg.offenders) / f'offender_{id}.jpg'), shot)
        self.registry.set_offender(id)
        print(f'Offender found: ID {id}, Plate {plate}, Speed {speed:.1f} km/h')
