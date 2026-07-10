import cv2
import os
import time

from warning_system import add_warning
from photo_capture import save_warning_photo

os.makedirs("captured_photos", exist_ok=True)

# Load Face Detection Model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

photo_count = 1

# No face timer
no_face_start = None

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # Face Found
    if len(faces) > 0:

        no_face_start = None

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            "Face Detected",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    # No Face
    else:

        cv2.putText(
            frame,
            "No Face",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

        if no_face_start is None:
            no_face_start = time.time()

        elif time.time() - no_face_start >= 5:

            warning = add_warning()

            save_warning_photo(frame, warning)

            no_face_start = time.time()

    cv2.imshow("Online Exam Monitoring", frame)

    key = cv2.waitKey(1) & 0xFF

    # Manual photo
    if key == ord("s"):

        filename = f"captured_photos/photo_{photo_count}.jpg"

        cv2.imwrite(filename, frame)

        print("Photo Saved")

        photo_count += 1

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()