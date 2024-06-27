from flask import Blueprint, jsonify, request, session
import sys
from functools import wraps
sys.path.append("..") # Adds higher directory to python modules path.
from src.db import players
from sqlalchemy.exc import IntegrityError
from connectors.mysql_connector import connection
from models import UserModel
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, login_required


import copy

users_bp = Blueprint('users', __name__)

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

@users_bp.post("/register")
def register_user():
    data = request.get_json()
    validate_user_register_data(data)
    user = UserModel(**data)
    Session = sessionmaker(connection)
    user.set_password(data['password'])
    try:
        with Session() as s:
            s.add(user)
            s.commit()
    except IntegrityError:
        raise CustomException("Duplicate Email Detected", 422)
    data.pop('password', None)
    return jsonify({"user": data}), 201

@users_bp.post("/login")
@handle_custom_exceptions
def login():
    data = request.get_json()
    validate_user_login_data(data)
    Session = sessionmaker(connection)
    with Session() as s:
        email = data['email']
        password = data['password']
        user = s.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            raise CustomException(f"User not found!", 400)
        
        if not user.check_password(password):
            return { "message": "Invalid password" }, 403
        
        login_user(user)

        # Get Session ID
        session_id = request.cookies.get('session')
        return jsonify({"session_id": session_id, "message": "Login Success"}), 200
    
@users_bp.route('/logout', methods=['GET'])
@login_required
def user_logout():
    logout_user()
    response = jsonify({"message": "Successfully logged out"})
    return response, 200
    

def validate_user_register_data(data):
    required_fields = ['email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            raise CustomException("Ensure User's email, password and role is provided!", 422)
        
        if not data[field]:
            raise CustomException("Ensure User's email, password and role is provided!", 422)
        
def validate_user_login_data(data):
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            raise CustomException("Ensure User's email and password are provided!", 422)
        
        if not data[field]:
            raise CustomException("Ensure User's email and password are provided!!", 422)
