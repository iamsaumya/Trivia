import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

''' It takes list of questions as an argument and return a random question'''


def get_random_question(questions):
    return questions[random.randrange(0, len(questions))]


''' This function is used to bifurcate questions to different pages for better UX '''


def paginate(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    paginated_questions = [question.format() for question in questions]

    return paginated_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        ''' Allowing these headers in requests'''
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        ''' Allowing these request methods '''
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()  # Querying the database to get all categories

        if(len(categories) == 0):  # checking if the len is 0, then give 404 error
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()

        if (len(questions) == 0):
            abort(404)

        # Paginate the questions in 10 on each page
        paginated = paginate(request, questions)

        categories = Category.query.all()

        return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(questions),
            'categories': {category.id: category.type for category in categories}
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)
        # try:
        if question is None:  # If NoneType object is return then abort(404)
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        # Check of searchTerm in the body of the request if it is present then the post request is to search for  a questions
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')

            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            if (len(questions) == 0):
                abort(404)

            paginated = paginate(request, questions)

            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        else:
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')

            if ((new_question is None) or (new_answer is None)
                    or (new_difficulty is None) or (new_category is None)):  # If any of these are not present give 422 error
                abort(422)

            try:
                question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
                question.insert()

                questions = Question.query.all()
                paginated = paginate(request, questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'question': question.format()
                })
            except:
                abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def categories_questions(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()  # Because category_id is stored as a str in the database
        except:
            abort(422)

        if (len(questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            # Using pyhthon trick to do operations in one line
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        body = request.get_json()

        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        if (len(previous_questions) == 5):
            return jsonify({
                'success': True
            })

        # If the type of the quiz is "click" THEN the quiz is for all
        if (quiz_category['type'] == 'click'):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()  # An excellent method notin_(), which saves 10 lines of code

        if (len(questions) == 0):
            return jsonify({
                'success': True
            })

        question = get_random_question(questions)

        return jsonify({
            'success': True,
            'question': question.format()
        })
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    return app
