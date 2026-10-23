# Traffic Violation Detector

Computer vision pipeline that detects vehicles from traffic cameras, estimates their speed, identifies those exceeding the speed limit, and reads their license plates

<img width="700" height="285" alt="result" src="https://github.com/user-attachments/assets/d8eb57f0-c564-4759-a7dd-91e37076a41e" />

## Features

- **Vehicle detection** with a fine-tuned YOLO model
- **ByteTrack** to keep a stable ID per vehicle
- **Speed estimation** via perspective transform and moving average the last N frames
- **Offender capture**: when a vehicle exceeds the speed limit, snapshot with the plate number and speed is saved
- **License plate OCR** on the offender crop

## How it works

1. YOLO + ByteTrack return a bounding box and ID for every vehicle
2. Point where the car touches the road is checked a calibrated zone
3. Points inside zone are mapped with a homography matrix
4. Distance between frames × meters-per-pixel × FPS gives speed, averaged over a sliding window to reduce delay
5. If average speed is at or above the limit, the vehicle is marked as offender. After that, a snapshot is taken and the plate is read

## Project structure

```

main.py
config.yaml
requirements.txt
data/
    config.yaml
    custom_bytetrack.yaml
    video.mp4
src/
    config.py
    geometry.py
    speed.py
    plate_number.py
    offenders.py
    visualization.py
    pipeline.py
ouput/
    offenders/
```


## Calibration

Speed accuracy depends directly on the zone calibration. Pick four points on the road that form a rectangle in the real world, and measure the real length of that rectangle along the direction of travel (`area_length`). The aspect ratio of `warp_size` should match the real width/length ratio of the zone, otherwise diagonal movement will be distorted

## Limitations

- OCR currently uses Apple Vision (`ocrmac`), so plate reading works on macOS only. It runs on the whole vehicle crop rather than a dedicated plate detector
- Single camera, fixed viewpoint, flat road

## Roadmap

- [ ] Violation logging (CSV / SQL)
- [ ] Unit tests for geometry and speed
- [ ] REST API (FastAPI)
- [ ] Docker image
- [ ] ONNX export

## Tech stack

Python, OpenCV, Ultralytics YOLO, ByteTrack, NumPy
