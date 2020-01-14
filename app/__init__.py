import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from config import config

print(f'current dir: {os.getcwd()}')

db = SQLAlchemy()
migrate = Migrate()


def create_app(object_name):
    """
    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import stat
    from . import survey

    app.register_blueprint(survey.bp)
    app.register_blueprint(stat.bp)

    return app
