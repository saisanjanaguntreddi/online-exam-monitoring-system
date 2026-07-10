import cv2
import os
import time

from warning_system import add_warning
from photo_capture import save_warning_photo

# Create folder if it doesn't exist
os.makedirs("captured_photos", exist_ok=True)

# Load Face Detection Model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

photo_count = 1

# Timers
no_face_start = None
multiple_face_start = None

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

    # ==========================
    # MULTIPLE FACE DETECTION
    # ==========================
    if len(faces) > 1:

        cv2.putText(
            frame,
            "WARNING : Multiple Faces Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        # Draw rectangles around all faces
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

        no_face_start = None

        if multiple_face_start is None:
            multiple_face_start = time.time()

        elif time.time() - multiple_face_start >= 5:

            warning = add_warning()
            save_warning_photo(frame, warning)

            multiple_face_start = time.time()

    # ==========================
    # SINGLE FACE
    # ==========================
    elif len(faces) == 1:

        no_face_start = None
        multiple_face_start = None

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
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # ==========================
    # NO FACE DETECTION
    # ==========================
    else:

        multiple_face_start = None

        cv2.putText(
            frame,
            "No Face",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        if no_face_start is None:
            no_face_start = time.time()

        elif time.time() - no_face_start >= 5:

            warning = add_warning()
            save_warning_photo(frame, warning)

            no_face_start = time.time()

    # Show Camera
    cv2.imshow("Online Exam Monitoring", frame)

    key = cv2.waitKey(1) & 0xFF

    # Manual Photo Capture
    if key == ord("s"):

        filename = f"captured_photos/photo_{photo_count}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Photo Saved : {filename}")

        photo_count += 1

    # Quit
    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()