from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from pybreaker import CircuitBreaker

from flask_cors import CORS

from consulate import Consul
from consulate.models import agent
import socket


db = SQLAlchemy()

circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=1000)

consul = Consul(host="consul")

def create_app():

    app = Flask(__name__)
    load_dotenv()

    serviceip = socket.gethostbyname(socket.gethostname())

    checks = agent.Check(
        name="alpha",
        http="https://alpha.ingesoftcurso.localhost/healtcheck",
        interval="10s",
        tls_skip_verify=True,
        timeout="1s",
        status="passing"
    )

    import uuid
    def generate_code():
        return str(uuid.uuid4()).replace('-', '').upper()[0:6]
    
    # limpiar todos los servicios registrados
    def deregister_services():
        services = consul.agent.services()
        for service_id in services:
            consul.agent.service.deregister(service_id)

    # deregister_services()

    # registrar servicio
    consul.agent.service.register(
        name="alpha",
        service_id=f"alpha_{generate_code()}",
        address=serviceip,
        tags=[
            "traefik.enable=true",
            "traefik.http.routers.alpha.rule=Host(`alpha.ingesoftcurso.localhost`)",
            "traefik.http.routers.alpha.tls=true",
            "traefik.http.services.alpha.loadbalancer.server.port=5000",
            "traefik.docker.network=red",
            "traefik.http.middlewares.latency-check.circuitbreaker.expression=LatencyAtQuantileMS(50.0) > 100",
            "traefik.http.services.alpha.loadbalancer.server.scheme=http"
        ],
        checks=[checks]
    )

    keyshipping = consul.kv
    HOST = keyshipping.get('alpha/DB_HOST')
    USER = keyshipping.get('alpha/DB_USER')
    PASSWORD = keyshipping.get('alpha/DB_PASSWORD')
    PORT = keyshipping.get('alpha/DB_PORT')
    DB_NAME = keyshipping.get('alpha/DB_DATABASE')

    # HOST = os.getenv('DB_HOST')
    # USER = os.getenv('DB_USER')
    # PASSWORD = os.getenv('DB_PASSWORD')
    # PORT = os.getenv('DB_PORT')
    # DB_NAME = os.getenv('DB_DATABASE')

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