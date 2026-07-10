import cv2
import os

os.makedirs("captured_photos", exist_ok=True)


def save_warning_photo(frame, warning_number):

    filename = f"captured_photos/warning_{warning_number}.jpg"

    cv2.imwrite(filename, frame)

    print(f"Warning Photo Saved : {filename}")