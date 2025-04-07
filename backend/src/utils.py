import base64
import cv2
import numpy as np

def decode_base64_image(base64_string):
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        img_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        return None
