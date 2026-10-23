from src.config import load_config
from src.pipeline import Pipeline


def main():
    Pipeline(load_config('config.yaml'), show=True).run()


if __name__ == '__main__':
    main()
