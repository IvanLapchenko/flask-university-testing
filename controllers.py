from flask import flash
from models import session, Question, Exam, User

def create_user(name, username, status, password):
    try:
        new_user = User(name=name, username=username, status=status, password=password)
        session.add(new_user)
        session.commit()
        flash('User created successfully', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error creating user: {str(e)}', 'error')

def create_exam(name):
    try:
        new_exam = Exam(name=name)
        session.add(new_exam)
        session.commit()
        flash('Exam created successfully', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error creating exam: {str(e)}', 'error')

def create_question(exam_id, question, answer1, answer2, correct):
    try:
        new_question = Question(exam_id=exam_id, question=question, answer1=answer1, answer2=answer2, correct=correct)
        session.add(new_question)
        session.commit()
        flash('Question created successfully', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error creating question: {str(e)}', 'error')

def get_all_exam_names():
    try:
        # exam_names = [exam.name for exam in session.query(Exam).all()]
        exam_names = session.query(Exam).all()
        return exam_names
    except Exception as e:
        flash(f'Error retrieving exam names: {str(e)}', 'error')
        return []
    
def get_questions_for_exam(exam_id):
    try:
        questions = session.query(Question).filter_by(exam_id=exam_id).all()
        questions_dict = {}

        for question_obj in questions:
            question_text = question_obj.question
            answers = {
                'answer1': question_obj.answer1,
                'answer2': question_obj.answer2,
            }
            correct_answer = question_obj.correct
            
            questions_dict[question_text] = {'answers': answers, 'correct_answer': correct_answer}

        return questions_dict
    except Exception as e:
        flash(f'Error retrieving questions for exam: {str(e)}', 'error')
        return []
    
def get_user_by_id(user_id):
    try:
        user = session.query(User).get(user_id)
        return user
    except Exception as e:
        flash(f'Error retrieving user: {str(e)}', 'error')
        return None

def count_correct_answers(user_answers: dict) -> tuple:
    correct_answers = session.query(Question.correct).filter_by(exam_id=user_answers["exam_id"]).all()
    number_of_correct_answers = 0
    if len(user_answers) < len(correct_answers):
        return False, 0
    for i in correct_answers:
        if i in user_answers.values:
            number_of_correct_answers += 1

    if number_of_correct_answers / len(correct_answers) > 0.75:
        return True, number_of_correct_answers
    return False, number_of_correct_answers

def get_all_exams():
    return session.query(Exam).all()