import json
import numpy as np
import cv2
from filetype import guess_mime
from enum import Enum, unique

from object_detector.yolo.yolo_detector import yolo as detector


@unique
class SupportedTypes(Enum):
    """Supported file types"""
    jpg = "image/jpeg"
    png = "image/png"


def validate_file_type(buffer: bytes):
    mime = guess_mime(buffer)
    if mime is None:
        raise TypeError("File type not supported.")
    return SupportedTypes(mime)


def decode_image(buffer: bytes):
    return cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), flags=cv2.IMREAD_COLOR)


def scan_buffer(buffer: bytes) -> str:
    mime_type = validate_file_type(buffer)
    image = decode_image(buffer)
    detector_out = json.loads(detector(image))

    scan_output = {
        "buffer_size": len(buffer),
        "mime_type": mime_type.value,
        "res_y": image.shape[0],
        "res_x": image.shape[1],
        "channels": image.shape[2],
        "objects": detector_out,
    }

    return json.dumps(scan_output, indent=4)
