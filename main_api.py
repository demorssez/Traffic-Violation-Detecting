from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from src.logger_config import setup_logger
from src.pipeline import Pipeline
from src.config import load_config
from pydantic import BaseModel
from pathlib import Path
import threading
import csv

setup_logger()

class PutData(BaseModel):
    file_path: str
    config_path: str
    
    
app = FastAPI(title='Traffic Violations API')
lock = threading.Lock()

def run_job(video, config):
    with lock:
        cfg = load_config(config)
        detector = Pipeline(cfg, show=False, write=False)
        detector.run(video)


@app.get('/offenders/')
def read_offenders(cfg: str = 'data/config.yaml'):
    config = load_config(cfg)
    if not Path(config.csv_path).exists():
        return []
    
    with open(Path(config.csv_path), encoding='utf-8') as f:
        return list(csv.DictReader(f))


@app.get('/offenders/{id}/image/')
def image_offender(id : int):
    path = Path('output/offenders') / f'offender_{id}.jpg'
    if not path.exists():
        raise HTTPException(404, 'Not Found')
    return FileResponse(path)
    

@app.post('/video_process')
def start_proccessing(data: PutData, background: BackgroundTasks):
    if not Path(data.file_path).exists():
        raise HTTPException(404, 'Not Found')
    
    background.add_task(run_job, data.file_path, data.config_path)
    return {'Status' : 'Processing'}


@app.get('/logs/')
def read_logs(logs_path: str = 'logs/info.log'):
    with open(Path(logs_path), 'r', encoding='utf-8') as f:
        return f.read()