from dataclasses import dataclass
import yaml

@dataclass
class Config:
    model_path: str
    track_path: str
    video_path: str
    output_path: str
    offenders: str
    speed_limit: float
    area_length: float
    area_points: list
    warp_size: list
    speed_window: int
    min_samples: int
    
    
def load_config(path: str = 'config.yaml'):
    with open(path, encoding='utf-8') as f:
        return Config(**yaml.safe_load(f))