import os

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from config import Config
from models import db, Student


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# Create database tables automatically when the application starts
with app.app_context():
    db.create_all()


# ── Health check ───────────────────────────────────────────────────────────

@app.route("/health")
def health_check():
    return {"status": "ok"}, 200


# ── READ: Show all students ────────────────────────────────────────────────

@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)


# ── CREATE: Add new student ────────────────────────────────────────────────

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()

        if not name or not email:
            flash("Name and Email are required!", "danger")
            return redirect(url_for("add_student"))

        student = Student(
            name=name,
            email=email,
            phone=phone,
            course=course,
        )

        try:
            db.session.add(student)
            db.session.commit()
            flash("Student added successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("A student with this email already exists!", "danger")
            return redirect(url_for("add_student"))

        return redirect(url_for("index"))

    return render_template("add_student.html")


# ── UPDATE: Edit existing student ──────────────────────────────────────────

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Name and Email are required!", "danger")
            return redirect(url_for("edit_student", id=id))

        student.name = name
        student.email = email
        student.phone = request.form.get("phone", "").strip()
        student.course = request.form.get("course", "").strip()

        try:
            db.session.commit()
            flash("Student updated successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("A student with this email already exists!", "danger")
            return redirect(url_for("edit_student", id=id))

        return redirect(url_for("index"))

    return render_template("edit_student.html", student=student)


# ── DELETE: Remove a student ───────────────────────────────────────────────

@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "danger")

    return redirect(url_for("index"))


# ── Application entry point ────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=port,
    )