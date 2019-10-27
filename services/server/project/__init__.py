import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from project.api.models import MemDB


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):

    # init mock-data
    MemDB.init()

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    # db.init_app(app)
    # migrate.init_app(app, db)
    # it's hacking time :) we won't use a DB

    # register blueprints
    # from project.api.books import books_blueprint
    # app.register_blueprint(books_blueprint)

    from project.api.draft import draft_blueprint
    app.register_blueprint(draft_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        # return {'app': app, 'db': db}
        return {'app': app}

    return app
