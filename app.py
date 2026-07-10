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

        # Check Duplicate Email
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

        # Insert Candidate
        cursor.execute(
            """
            INSERT INTO candidate(full_name,email,exam_name)
            VALUES(?,?,?)
            """,
            (full_name, email, exam_name)
        )

        connection.commit()

        candidate_id = cursor.lastrowid

        connection.close()

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

            return render_template(
                "login_success.html",
                candidate_name=candidate[1],
                candidate_id=candidate[0]
            )

        else:

            return """
            <script>

            alert("Invalid Candidate ID or Email");

            window.location='/login';

            </script>
            """

    return render_template("login.html")


# ---------------- EXAM INSTRUCTIONS ----------------

@app.route("/exam")
def exam():

    return render_template("exam.html")


# ---------------- QUESTIONS PAGE ----------------

@app.route("/questions")
def questions():

    return render_template("questions.html")


# ---------------- MAIN ----------------

if __name__ == "__main__":

    app.run(debug=True)