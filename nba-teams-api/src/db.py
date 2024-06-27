from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

teams = [ 
    {
        "id": 1,
        "name": "Los Angeles Lakers",
        "city": "Los Angeles"
    },
    {
        "id": 2,
        "name": "Golden State Warriors",
        "city": "San Fransisco"
    }
]

players = [
    {
        "id": 1,
        "name": "LeBron James",
        "team_id": 1,
        "age": 37
    },
    {
        "id": 2,
        "name": "Anthony Davis",
        "team_id": 1,
        "age": 30
    },
    {
        "id": 3,
        "name": "Stephen Curry",
        "team_id": 2,
        "age": 35
    },
    {
        "id": 4,
        "name": "Draymond Green",
        "team_id": 2,
        "age": 33
    }
]