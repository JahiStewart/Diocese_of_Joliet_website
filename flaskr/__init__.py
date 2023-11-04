import os

from flask import Flask, render_template

from flask_bootstrap import Bootstrap

# creates and configure the app
def create_app(test_config=None):
    # create flask instance
    app = Flask(__name__, instance_relative_config=True) # configuration files are relative to the instance folder
    Bootstrap(app)

    # default configuration
    app.config.from_mapping( 
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')

    # registers 'init_db' command with the app (use: flask --app flaskr init-db) 
    # CAUTION: this will clear existing data and create new tables
    from . import db
    db.init_app(app)

    # import and register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import nav
    nav.init_app(app)

    return app

# Create virtual environment
# py -m venv .venv

# Dependencies 
# pip install -r requirements.txt

# run flask app
# flask --app flaskr run --debug

