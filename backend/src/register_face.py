import cv2
import os
import uuid

DATASET_DIR = "backend/dataset"

def save_new_face(image, label):
    user_dir = os.path.join(DATASET_DIR, label)
    os.makedirs(user_dir, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(user_dir, file_name)
    cv2.imwrite(file_path, image)
    return file_path
