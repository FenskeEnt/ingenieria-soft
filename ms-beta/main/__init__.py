from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

from flask_caching import Cache

db = SQLAlchemy()

cache = Cache()

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

    # redis config
    app.config['CACHE_TYPE'] = os.getenv("CACHE_TYPE")
    app.config["CACHE_REDIS_URL"] = os.getenv("CACHE_REDIS_URL")

    cache.init_app(app)

    return app