from flask import Flask, render_template, request, jsonify
import sqlite3
import subprocess
import sys
import os
import base64
import numpy as np
import cv2
print("Current Folder:", os.getcwd())
print("Static Folder Exists:", os.path.exists("static/js/monitor.js"))
print("Static Folder Contents:", os.listdir("static"))
print("JS Folder Exists:", os.path.exists("static/js"))

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
os.makedirs("captured_photos", exist_ok=True)
import time

warning_count = 0

no_face_start = None
multiple_face_start = None

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        exam_name = request.form["exam_name"]

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            return """
            <script>
            alert("Passwords do not match.");
            window.location='/register';
            </script>
            """

        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("database/exam.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM candidate WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            connection.close()

            return """
            <script>
            alert("This Email is Already Registered.");
            window.location='/login';
            </script>
            """

        cursor.execute(
            """
            INSERT INTO candidate
            (full_name,email,exam_name,password)
            VALUES(?,?,?,?)
            """,
            (
                full_name,
                email,
                exam_name,
                hashed_password
            )
        )

        connection.commit()

        candidate_id = cursor.lastrowid

        connection.close()

        subprocess.run([
            sys.executable,
            "monitoring/registration_photo.py",
            str(candidate_id)
        ])

        return render_template(
            "register_success.html",
            candidate_id=candidate_id
        )

    return render_template("register.html")
# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        candidate_id = request.form["candidate_id"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/exam.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM candidate
            WHERE id=? AND email=?
            """,
            (candidate_id, email)
        )

        candidate = cursor.fetchone()

        connection.close()

        if candidate:

            if check_password_hash(candidate[5], password):

                return render_template(
                    "login_success.html",
                    candidate_name=candidate[1],
                    candidate_id=candidate[0]
                )

            else:

                return """
                <script>
                alert("Incorrect Password");
                window.location='/login';
                </script>
                """

        else:

            return """
            <script>
            alert("Invalid Candidate ID or Email");
            window.location='/login';
            </script>
            """

    return render_template("login.html")


# ---------------- EXAM ----------------

@app.route("/exam")
def exam():

    return render_template("exam.html")


# ---------------- START EXAM ----------------

@app.route("/start_exam")
def start_exam():

    return render_template("questions.html")


# ---------------- QUESTIONS ----------------

@app.route("/questions")
def questions():

    return render_template("questions.html")
# ---------------- TAB WARNING ----------------

@app.route("/tab_warning", methods=["POST"])
def tab_warning():

    global warning_count

    warning_count += 1

    return jsonify({

        "warning_count": warning_count,
        "message": "Browser Tab Switched"

    })

# ---------------- FACE DETECTION API ----------------
@app.route("/detect_face", methods=["POST"])
def detect_face():

    global warning_count
    global no_face_start
    global multiple_face_start

    data = request.get_json()

    image_data = data["image"].split(",")[1]

    image_bytes = base64.b64decode(image_data)

    np_array = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    response = {
        "faces": len(faces),
        "warning": False,
        "warning_count": warning_count,
        "message": "Face Detected"
    }

    # ---------- SINGLE FACE ----------
    if len(faces) == 1:

        no_face_start = None
        multiple_face_start = None

    # ---------- NO FACE ----------
    elif len(faces) == 0:

        multiple_face_start = None

        if no_face_start is None:
            no_face_start = time.time()

        elif time.time() - no_face_start >= 5:

            warning_count += 1
            filename = f"captured_photos/warning_{warning_count}.jpg"

            cv2.imwrite(filename, frame)

            response["warning"] = True
            response["warning_count"] = warning_count
            response["message"] = "No Face Detected"

            no_face_start = time.time()

    # ---------- MULTIPLE FACES ----------
    else:

        no_face_start = None

        if multiple_face_start is None:
            multiple_face_start = time.time()

        elif time.time() - multiple_face_start >= 5:

            warning_count += 1
            filename = f"captured_photos/warning_{warning_count}.jpg"

            cv2.imwrite(filename, frame)
            response["warning"] = True
            response["warning_count"] = warning_count
            response["message"] = "Multiple Faces Detected"

            multiple_face_start = time.time()

    return jsonify(response)
# ---------------- MAIN ----------------

if __name__ == "__main__":

    app.run(debug=True)