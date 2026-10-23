import numpy as np
from PIL import Image
from ocrmac import ocrmac


def read_plate(crop_frame):
    crop_pil = Image.fromarray(crop_frame[:, :, ::-1])
    result = ocrmac.OCR(crop_pil).recognize()
    return ''.join(line[0].replace(' ', '') for line in result)
