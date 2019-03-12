from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    from .graph import graph as graph_blueprint
    app.register_blueprint(graph_blueprint, url_prefix='/graphx')
    from .data import data as data_blueprint
    app.register_blueprint(data_blueprint, url_prefix='/data')
    from .project import project as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/project')


    return app
