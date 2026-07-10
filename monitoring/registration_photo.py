import cv2
import os
import sys

# Get Candidate ID from app.py
candidate_id = sys.argv[1]

# Create folder
os.makedirs("candidate_photos", exist_ok=True)

camera = cv2.VideoCapture(0)

print("Press SPACE to Capture Photo")
print("Press Q to Quit")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    cv2.putText(
        frame,
        "Press SPACE to Capture",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.imshow("Candidate Registration", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 32:

        filename = f"candidate_photos/candidate_{candidate_id}.jpg"

        cv2.imwrite(filename, frame)

        print("Photo Saved Successfully")

        break

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()