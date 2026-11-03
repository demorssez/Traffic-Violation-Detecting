from src.config import load_config
from src.pipeline import Pipeline


def main():
    Pipeline(load_config('/data/config.yaml'), show=True).run('/data/Traffic_IP_Camera_video.mp4')


if __name__ == '__main__':
    main()
