import cv2
import os

# Create folder if it doesn't exist
os.makedirs("captured_photos", exist_ok=True)

# Load Face Detection Model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

photo_count = 1

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect Faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # Draw Rectangle
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Online Exam Monitoring", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press S to capture photo
    if key == ord('s'):
        filename = f"captured_photos/photo_{photo_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Photo Saved: {filename}")
        photo_count += 1

    # Press Q to quit
    elif key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()