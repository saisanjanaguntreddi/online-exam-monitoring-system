from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


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

        connection = sqlite3.connect("database/exam.db")
        cursor = connection.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM candidate WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return """
            <h2>This Email is Already Registered.</h2>
            <a href="/login">
                <button>Go to Login</button>
            </a>
            """

        # Register Candidate
        cursor.execute("""
            INSERT INTO candidate(full_name, email, exam_name)
            VALUES(?,?,?)
        """, (full_name, email, exam_name))

        connection.commit()

        candidate_id = cursor.lastrowid

        connection.close()

        return f"""
        <h2>Registration Successful!</h2>

        <h3>Your Candidate ID : {candidate_id}</h3>

        <p>Please save your Candidate ID for Login.</p>

        <h4>Session Status : Not Started</h4>

        <a href="/login">
            <button>Go to Login</button>
        </a>
        """

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        candidate_id = request.form["candidate_id"]
        email = request.form["email"]

        connection = sqlite3.connect("database/exam.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM candidate
            WHERE id=? AND email=?
        """, (candidate_id, email))

        candidate = cursor.fetchone()

        connection.close()

        if candidate:

            return f"""
            <h2>Login Successful!</h2>

            <h3>Welcome {candidate[1]}</h3>

            <h4>Candidate ID : {candidate[0]}</h4>

            <a href="/exam">
                <button>Proceed to Exam</button>
            </a>
            """

        else:

            return """
            <h2>Invalid Candidate ID or Email</h2>

            <a href="/login">
                <button>Try Again</button>
            </a>
            """

    return render_template("login.html")


# ---------------- EXAM ----------------

@app.route("/exam")
def exam():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Online Exam</title>

        <style>

            body{
                font-family:Arial;
                text-align:center;
                margin-top:40px;
            }

            button{
                padding:12px 20px;
                margin:10px;
                font-size:16px;
            }

        </style>

    </head>

    <body>

        <h1>Online Examination</h1>

        <h2>Exam Instructions</h2>

        <ul style="display:inline-block;text-align:left;">

            <li>Keep your camera ON.</li>

            <li>Do not switch browser tabs.</li>

            <li>No mobile phones allowed.</li>

            <li>Do not leave your seat during the examination.</li>

            <li>Follow all examination rules.</li>

        </ul>

        <br><br>

        <h3>Session Status : Not Started</h3>

        <button onclick="alert('Exam Started')">
            Start Exam
        </button>

        <button onclick="alert('Exam Paused')">
            Pause Exam
        </button>

        <button onclick="alert('Exam Resumed')">
            Resume Exam
        </button>

        <button onclick="alert('Exam Submitted Successfully')">
            Submit Exam
        </button>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)