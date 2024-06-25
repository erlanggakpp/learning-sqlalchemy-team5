from flask import Blueprint, jsonify, request
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
from flasgger import swag_from
from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from connectors.mysql_connector import connection
from models import TeamModel
from sqlalchemy.orm import sessionmaker, joinedload
team_bp = Blueprint('teams', __name__)

class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

def handle_custom_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": e.message}), e.error_code
    return decorated_function

@team_bp.get("/")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'get_teams.yml'))
@handle_custom_exceptions
def get_teams():
    Session = sessionmaker(connection)
    teams = []
    with Session() as s:
        query = s.query(TeamModel).options(joinedload(TeamModel.players))
        name = request.args.get('name')
        city = request.args.get('city')
        if name: 
            query = query.filter(TeamModel.name.ilike(f'%{name}%'))
        if city: 
            query = query.filter(TeamModel.city.ilike(f'%{name}%'))
        teams = query.all()
    if len(teams) == 0:
        raise CustomException("There are no registered teams yet", 400)
    return jsonify({"teams": [team.to_dict() for team in teams]}), 200
    
@team_bp.post("/")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'create_teams.yml'))
@handle_custom_exceptions
def create_teams():
    data = request.get_json()
    validate_team_data(data)
    team = TeamModel(**data)
    Session = sessionmaker(connection)
    try:
        with Session() as s:
            s.add(team)
            s.commit()
    except IntegrityError:
        raise CustomException("Duplicate Name Detected", 422)
    return jsonify({"team": data}), 201

@team_bp.get("/<int:id>")
@handle_custom_exceptions
def get_specific_team(id):
    Session = sessionmaker(connection)
    target_team = None
    with Session() as s:
        target_team = s.query(TeamModel).options(joinedload(TeamModel.players)).get(id)
        print(target_team)
    if target_team is None:
        raise CustomException(f"There are no registered teams with ID: {id}", 400)
    return jsonify({"team": target_team.to_dict()}), 200
    
@team_bp.put("/<int:id>")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'edit_teams.yml'))
@handle_custom_exceptions
def edit_specific_team(id):
    data = request.get_json()
    validate_team_data(data)
    Session = sessionmaker(connection)
    target_team = None
    try:
        with Session() as s:
            target_team = s.query(TeamModel).get(id)
            print(target_team)
            if target_team is None:
                raise CustomException(f"There are no registered teams with ID: {id}", 400)
            for key, value in data.items():
                if hasattr(target_team, key):
                    setattr(target_team, key, value)
            s.commit()
    except IntegrityError:
        raise CustomException("Duplicate Name Detected", 422)
    return jsonify({"message": f"Sucessfully edited team with ID: {id}"}), 200

    
def validate_team_data(data):
    required_fields = ['name', 'city', 'arena']
    for field in required_fields:
        if field not in data:
            raise CustomException("Ensure Team's name, city and arena is provided!", 422)
        
        if not data[field]:
            raise CustomException("Ensure Team's name, city and arena values are correct!", 422)
        


