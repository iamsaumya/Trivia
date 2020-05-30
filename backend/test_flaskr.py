import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
            "question": "A test question",
            "answer": "A test answer",
            "difficulty": 1,
            "category": 1
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        question = Question(question=self.question['question'], answer=self.question['answer'],
                            difficulty=self.question['difficulty'], category=self.question['category'])
        question.insert()

        question_id = question.id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(data['success'], True)

    def test_error_delete_question(self):

        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_question_search(self):
        res = self.client().post(
            '/questions', json={"searchTerm": "test"})
        data = json.loads(res.data)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_error_question_search(self):
        res = self.client().post(
            '/questions', json={"searchTerm": "testing"})
        data = json.loads(res.data)

        self.assertEqual(data['message'], 'Resource not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])

    def test_error_add_question(self):

        self.question.pop('question')
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)

    def test_categories_questions(self):

        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_error_categories_questions(self):

        res = self.client().get('categories/10/questions')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Resource not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        res = self.client().post("/quizzes",
                                 json={"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_error_quizzes(self):
        res = self.client().post("/quizzes",
                                 json={"quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)

        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
