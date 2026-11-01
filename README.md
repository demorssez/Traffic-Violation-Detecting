# Traffic Violation Detector

Computer vision pipeline that detects vehicles from traffic cameras, estimates their speed, identifies those exceeding the speed limit, and reads their license plates

<img width="700" height="285" alt="result" src="https://github.com/user-attachments/assets/d8eb57f0-c564-4759-a7dd-91e37076a41e" />

## Features

- **Vehicle detection** with a fine-tuned YOLO model
- **ByteTrack** to keep a stable ID per vehicle
- **Speed estimation** via perspective transform and moving average the last N frames
- **Offender capture**: when a vehicle exceeds the speed limit, snapshot with the plate number and speed is saved
- **License plate OCR** on the offender crop
- **Code is logged**, and violators are recorded in a separate CSV file

## How it works

1. YOLO + ByteTrack return a bounding box and ID for every vehicle
2. Point where the car touches the road is checked a calibrated zone
3. Points inside zone are mapped with a homography matrix
4. Distance between frames × meters-per-pixel × FPS gives speed, averaged over a sliding window to reduce delay
5. If average speed is at or above the limit, the vehicle is marked as offender. After that, a snapshot is taken and the plate is read

## Calibration

Speed accuracy depends directly on the zone calibration. Pick four points on the road that form a rectangle in the real world, and measure the real length of that rectangle along the direction of travel (`area_length`). The aspect ratio of `warp_size` should match the real width/length ratio of the zone, otherwise diagonal movement will be distorted

## Limitations

- OCR currently uses Apple Vision (`ocrmac`), so plate reading works on macOS only. It runs on the whole vehicle crop rather than a dedicated plate detector
- Single camera, fixed viewpoint, flat road

## REST API

The pipeline can also be run as a service built with FastAPI.

```bash
uvicorn main_api:app --reload
```

docs: http://127.0.0.1:8000/docs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/video_process` | Start processing a video in the background. Body: `{"file_path": "data/video.mp4"}` |
| `GET` | `/offenders` | List of detected offenders (from the CSV log) |
| `GET` | `/offenders/{id}/image` | Evidence snapshot for the offender with the given track ID |
| `GET` | `/logs` | Latest application log lines |

Example:

```bash
curl -X POST http://127.0.0.1:8000/video_process \
  -H "Content-Type: application/json" \
  -d '{"file_path": "data/Traffic_IP_Camera_video.mp4"}'

curl http://127.0.0.1:8000/offenders
```

Processing runs in a background task, so the `POST` returns immediately. Only one video is processed at a time; other requests wait in a queue.

## Web UI

Streamlit dashboard on top of the API: start processing, watch the logs, browse offenders and open their snapshots.

For interaction with API and Visual dashboard: http://localhost:8501/

```bash
uvicorn main_api:app --reload & streamlit run visual.py
```

## Update

- Added code logging to 'logs' folder and recorded violators into a CSV file
- API
- Streamlit dashboard

## Roadmap

- [x] Violation logging (CSV / SQL)
- [x] REST API (FastAPI)
- [x] WEB interface for interaction
- [ ] Docker image
- [ ] ONNX export

## Tech stack

Python, OpenCV, Ultralytics YOLO, ByteTrack, NumPy, FastAPI
