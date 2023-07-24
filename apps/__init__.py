from flask import Flask
import apps.routes as routes
from .config_app import config
from .database import db
from .marshmallow import ma

app = Flask(__name__)

def init_app()-> Flask:
    if config['mode'] == 'dev':
        app.config.from_object(config['development'])
    if config['mode'] == 'prod':
        app.config.from_object(config['production'])


    db.init_app(app)
    ma.init_app(app)
    
    import apps.models

    app.register_blueprint(routes.tp_route)
    app.register_blueprint(routes.auth_route)
    app.register_blueprint(routes.tareas_route)


    with app.app_context():
        db.create_all()

    return app