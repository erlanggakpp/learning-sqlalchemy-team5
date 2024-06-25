from flask import Flask, jsonify
from controllers.teams import team_bp
from controllers.players import player_bp
from flasgger import Swagger
from os import environ
from dotenv import load_dotenv
from db import db
from flask_migrate import Migrate
from connectors.mysql_connector import connection, engine
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

# Ini untuk load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root@localhost:3306/revou_team5'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)


    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/api-docs/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs/"
    }
    swagger = Swagger(app, config=swagger_config)  # Initialize Flasgger

    app.register_blueprint(team_bp, url_prefix='/teams')
    app.register_blueprint(player_bp, url_prefix='/players')
    @app.route('/hello/', methods=['GET', 'POST'])
    def welcome():
        # cara menggunakan .env
        SECRET_KEY = environ.get('SECRET_KEY')
        API_KEY = environ.get('API_KEY')    
        return f"Hello! API_KEY: {API_KEY}. SECRET_KEY: {SECRET_KEY}"
    with app.app_context():
        db.create_all()
    return app





if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



#COMMAND LIST
# pipenv run flask db init 
# pipenv run flask db migrate -m "Initial migration." 
# pipenv run flask db upgrade