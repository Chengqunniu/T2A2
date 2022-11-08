from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.user_controller import user_bp
import os


def create_app():
    app = Flask(__name__)

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400


    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False # allow field displayed in the same order of fields in class meta
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')    

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(user_bp)



    return app
