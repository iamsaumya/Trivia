# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API

### Introduction

This API is used by Trivia App frontend to fetch the data from database.

### Getting Started

1. Base URL
        The base URL of the API is ``` http://127.0.0.1:5000/ ```
1. Authentication
        The API does not require any authentication

### Error Handling

The API returns a JSON response with Success validation, Response code and a guiding message.

```JSON
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```

### Endpoints

GET '/categories'

- Fetches a dictionary of categories and success. In categories the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with keys, categories and sucess. Categories contains a object of id: category_string key:value pairs. Success is the validation of request from the server.

```URL
curl  http://127.0.0.1:5000/categories
```

``` JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```

GET '/questions'

- Fetches a dictionary of categories, questions,success and total_questions.
  - Categories will have id as key and type as value.
  - Questions have answer, category, difficulty, id and question as key and corresponding values.
- Request Arguments: None
- Returns: An object with all the categories, 10 questions that are paginated with total number of questions and success validation from server.

``` URL
curl  http://127.0.0.1:5000/questions
```

```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    ...
    ...
    ...
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

DELETE '/question/\<int:question_id\>'

- Deletes a question from the database. If the question does not exits, It returns 404 error.
- Path Parameter: Question Id.
- Returns: An object with success validation from server and the ID of the deleted question.

``` URL
curl  http://127.0.0.1:5000/questions/15 -X DELETE
````

```JSON
{
  "deleted": 15,
  "success": true
}
```

POST '/questions'

- Fetches a dictionary of questions,success and total_questions.
  - Questions have answer, category, difficulty, id and question as key and corresponding values.
- Request Arguments:
  - A JSON object with "searchTerm" to search a question in the database
  - A JSON object with question,answer,difficulty and category to create a question.
- Returns:
  - Request with searchTerm
  - A JSON object with list of questions that matched the searchTerm, success validation and total questions.
  - Request with questions parameters
  - A JSON object with created as question id, the question and success validation

```URL
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"world"}'
```

```JSON
{
  "questions": [
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

```URL
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is Naruto?","answer":"A feeling","difficulty":1,"category":5}'
```

```JSON
{
  "created": 29,
  "question": {
    "answer": "A feeling",
    "category": "5",
    "difficulty": 1,
    "id": 29,
    "question": "What is Naruto?"
  },
  "question_created": "What is Naruto?",
  "success": true
}
```

GET "categories/\<int:category_id\>/questions"

- Fetches a dictionary of with category_id as current_category, list of questions, success and total_questions.
- Request Arguments: None
- Returns: An object with current_category, list of questions, total number of questions and success validation from server.

```URL
curl 127.0.0.1:5000/categories/1/questions
```

```JSON
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

POST "/quizzes"

- Fetches a dictionary of with a random question and success.
- Request Arguments: A JSON object with a list of ids as previous_questions, and a dictionary as quiz_category with type and id of the requested category.
- Returns: An object with random question and success validation from server.

```URL
curl 127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'
```

```JSON
{
  "question": {
    "answer": "The Liver",
    "category": "1",
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
