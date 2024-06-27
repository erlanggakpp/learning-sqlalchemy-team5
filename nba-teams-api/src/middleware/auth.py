from functools import wraps
from flask_login import current_user

class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

def authenticator_and_authorization(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if current_user.is_authenticated == False:
                raise CustomException("Please Login first!", 403)
            
            if current_user.role != role:
                raise CustomException("You are not allowed to access this", 403)
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
