import os
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Student

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create database tables automatically when app starts
with app.app_context():
    db.create_all()


# ── READ: Show all students ────────────────────────────────────────────────
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


# ── CREATE: Add new student ────────────────────────────────────────────────
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name   = request.form['name']
        email  = request.form['email']
        phone  = request.form['phone']
        course = request.form['course']

        student = Student(name=name, email=email, phone=phone, course=course)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_student.html')


# ── UPDATE: Edit existing student ──────────────────────────────────────────
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name   = request.form['name']
        student.email  = request.form['email']
        student.phone  = request.form['phone']
        student.course = request.form['course']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)


# ── DELETE: Remove a student ───────────────────────────────────────────────
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)