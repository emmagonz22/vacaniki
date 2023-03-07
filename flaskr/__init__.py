from flaskr import pages

from flask import Flask

import logging
logging.basicConfig(level=logging.DEBUG)

# The flask terminal command inside "run-flask.sh" searches for
# this method inside of __init__.py (containing flaskr module 
# properties) as we set "FLASK_APP=flaskr" before running "flask".
def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)


    #Reference = "https://flask-login.readthedocs.io/en/latest/#how-it-works%20for%20more%20info"
    # Create a LoginManager instance
    login_manager = LoginManager()

    # Configure LoginManager
    login_manager.init_app(app)

    # Call methods on the login_manager instance as needed
    login_manager.login_view = 'login'

    # Define user_loader callback
    @login_manager.user_loader
    def load_user(username):
    # Retrieve user
        user_id = hashlib.blake2b(username.encode('utf-8')).hexdigest()
        return User.get(user_id)


    # This is the default secret key used for login sessions
    # By default the dev environment uses the key 'dev'
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # This file is not committed. Place it in production deployments.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # TODO(Project 1): Make additional modifications here for logging in, backends
    # and additional endpoints.
    pages.make_endpoints(app)
    return app
