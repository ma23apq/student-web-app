from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, course TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("index.html", students=students)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
