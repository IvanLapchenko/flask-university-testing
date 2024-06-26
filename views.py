from app import app
from random import randint
from models import User, session
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from controllers import count_correct_answers, create_question, get_all_exam_names, get_all_exams, get_questions_for_exam, create_user, create_exam


@app.route('/')
def home():
    return render_template('home.html', exams=get_all_exam_names())

@app.route('/ca')
def ca():
    create_user('admin', 'admin', 'teacher', 'admin')
    return redirect(url_for('home'))

@app.route('/exam/<int:exam_id>')
def exam(exam_id):
    exam_questions = get_questions_for_exam(exam_id)
    return str(exam_questions)
    if exam_questions:
        [test.insert(randint(1, 3), test.pop(3)) for test in exam_questions]
        return render_template('exam.html', exam_questions=exam_questions)
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/result')
@login_required
def result():
    is_passed, correct_answers = count_correct_answers(request.form)
    return render_template("result.html", correct_answers=correct_answers, passed=is_passed)


@app.route('/create_q', methods=['GET', 'POST'])
@login_required
def create_q():
    if request.method == 'POST':
        create_question(exam_id=request.form['exam_id'], question=request.form['question'], answer1=request.form['ans1'],
                         answer2=request.form['ans2'], correct=request.form['correct'])
        return redirect(url_for('home'))
    return render_template('create.html', exams=get_all_exams())


@app.route('/create_ex', methods=['GET', 'POST'])
@login_required
def create_ex():
    if request.method == 'POST':
        create_exam(name=request.form.get("name"))
        return redirect(url_for('home'))
    return render_template('create.html', exams=get_all_exams())