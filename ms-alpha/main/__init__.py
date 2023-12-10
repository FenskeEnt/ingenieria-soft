from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from pybreaker import CircuitBreaker

from flask_cors import CORS

db = SQLAlchemy()

circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=1000)

def create_app():

    app = Flask(__name__)
    load_dotenv()

    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_DATABASE')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8mb4'

    db.init_app(app)

    cors = CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # circuit_breaker = CircuitBreaker(app)

    # circuite breaker
    app.config['CIRCUITE_BREAKER'] = circuit_breaker

    return app