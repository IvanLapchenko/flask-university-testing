import unittest
from unittest.mock import patch, MagicMock
from flask import flash

# Імпортуємо функції, які будемо тестувати
from controllers import create_user, create_exam, create_question, \
    get_all_exam_names, get_questions_for_exam, get_user_by_id, \
    count_correct_answers, get_all_exams

class TestYourApp(unittest.TestCase):

    # Тестуємо функцію create_user
    def test_create_user(self):
        with patch('your_module.session') as mock_session:
            # Створюємо об'єкт користувача
            create_user('John Doe', 'john_doe', 'student', 'password123')

            # Перевіряємо, чи викликали методи session правильно
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

            # Перевіряємо, чи виведено правильне повідомлення flash
            flash.assert_called_once_with('User created successfully', 'success')

    # Тестуємо функцію create_exam
    def test_create_exam(self):
        with patch('your_module.session') as mock_session:
            # Створюємо об'єкт екзамену
            create_exam('Math Exam')

            # Перевіряємо, чи викликали методи session правильно
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

            # Перевіряємо, чи виведено правильне повідомлення flash
            flash.assert_called_once_with('Exam created successfully', 'success')

    # Тестуємо функцію create_question
    def test_create_question(self):
        with patch('your_module.session') as mock_session:
            # Створюємо об'єкт питання
            create_question(1, 'What is 2 + 2?', '4', '5', '6', '4')

            # Перевіряємо, чи викликали методи session правильно
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

            # Перевіряємо, чи виведено правильне повідомлення flash
            flash.assert_called_once_with('Question created successfully', 'success')

    # Тестуємо функцію get_all_exam_names
    def test_get_all_exam_names(self):
        with patch('your_module.session.query') as mock_query:
            # Симулюємо повернення списку екзаменів
            mock_query.return_value.all.return_value = [{'name': 'Math Exam'}, {'name': 'Physics Exam'}]

            # Отримуємо всі назви екзаменів
            exam_names = get_all_exam_names()

            # Перевіряємо, чи отримано правильні назви екзаменів
            self.assertEqual(exam_names, ['Math Exam', 'Physics Exam'])

    # Тестуємо функцію get_questions_for_exam
    def test_get_questions_for_exam(self):
        with patch('your_module.session.query') as mock_query:
            # Симулюємо повернення списку питань
            mock_query.return_value.filter_by.return_value.all.return_value = [
                MagicMock(question='What is 2 + 2?', answer1='4', answer2='5', answer3='6', correct='4'),
                MagicMock(question='What is 3 x 3?', answer1='6', answer2='9', answer3='12', correct='9')
            ]

            # Отримуємо питання для конкретного екзамену
            questions_dict = get_questions_for_exam(1)

            # Перевіряємо, чи отримано правильний словник питань
            self.assertEqual(questions_dict, {
                'What is 2 + 2?': {'answers': {'answer1': '4', 'answer2': '5', 'answer3': '6'}, 'correct_answer': '4'},
                'What is 3 x 3?': {'answers': {'answer1': '6', 'answer2': '9', 'answer3': '12'}, 'correct_answer': '9'}
            })

    # Тестуємо функцію get_user_by_id
    def test_get_user_by_id(self):
        with patch('your_module.session.query') as mock_query:
            # Симулюємо повернення об'єкта користувача
            mock_query.return_value.get.return_value = MagicMock(name='John Doe', username='john_doe', status='student')

            # Отримуємо користувача за його id
            user = get_user_by_id(1)

            # Перевіряємо, чи отримано правильний об'єкт користувача
            self.assertEqual(user.name, 'John Doe')
            self.assertEqual(user.username, 'john_doe')
            self.assertEqual(user.status, 'student')

    # Тестуємо функцію count_correct_answers
    def test_count_correct_answers(self):
        with patch('your_module.session.query') as mock_query:
            # Симулюємо повернення коректних відповідей для екзамену
            mock_query.return_value.filter_by.return_value.all.return_value = [('4',), ('9',)]

            # Оцінюємо кількість правильних відповідей
            is_passed, correct_answers = count_correct_answers({'exam_id': 1, 'question1': '4', 'question2': '9'})

            # Перевіряємо, чи отримано правильні результати
            self.assertTrue(is_passed)
            self.assertEqual(correct_answers, 2)

    # Тестуємо функцію get_all_exams
    def test_get_all_exams(self):
        with patch('your_module.session.query') as mock_query:
            # Симулюємо повернення списку екзаменів
            mock_query.return_value.all.return_value = [
                MagicMock(name='Math Exam'),
                MagicMock(name='Physics Exam')
            ]

            # Отримуємо всі екзамени
            exams = get_all_exams()

            # Перевіряємо, чи отримано правильний список екзаменів
            self.assertEqual(exams, [
                {'name': 'Math Exam'},
                {'name': 'Physics Exam'}
            ])

if __name__ == '__main__':
    unittest.main()
