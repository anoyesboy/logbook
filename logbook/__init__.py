from flask import Flask
from flask_wtf.csrf import CSRFProtect
from logbook.database import db
import os


csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config == None:
        app.config.from_mapping(
                SECRET_KEY=os.environ.get("SECRET_KEY"),
                SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
                WTF_CSRF_SECRET_KEY=os.environ.get("CSRF_SECRET_KEY"),
                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                )
    else:
        app.config.from_mapping(test_config)


    db.init_app(app)
    csrf.init_app(app)


    from logbook.blueprints import logbook
    app.register_blueprint(logbook.bp)
    app.add_url_rule("/", endpoint="index")

    from logbook.blueprints import flight
    app.register_blueprint(flight.bp, url_prefix="/flight")

    from logbook.blueprints import auth
    app.register_blueprint(auth.bp, url_prefix="/auth")

    from logbook.blueprints import airport
    app.register_blueprint(airport.bp, url_prefix="/airport")

    from logbook.blueprints import airplane
    app.register_blueprint(airplane.bp, url_prefix="/airplane")


    return app
