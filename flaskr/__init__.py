from . import db, auth, forms, reservations

import os

from flask import Flask, render_template, session

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

    # registers 'init_db' command with the app (use: flask --app flaskr init-db) 
    # CAUTION: this will clear existing data and create new tables
    db.init_app(app)

    # import and register auth blueprint
    app.register_blueprint(reservations.reservations)
    app.register_blueprint(auth.auth)
    app.register_blueprint(forms.forms)

    
    @app.route('/myaccount')
    def myaccount():
        # create connection to database
        database = db.get_db()
        # get current users id
        user_id = session.get('user_id')
        # get users organization if any
        org = database.execute(
            'SELECT * FROM organization WHERE id = ?',
            (user_id,)
        ).fetchone()
        # catch error in case user has no organization
        try:
            org_name = org['name']
        except:
            org_name = "You currenlty don't belong to any organizations."

        pending_reservations_info = reservations.get_reservations('N', user_id)
        approved_reservations_info = reservations.get_reservations('Y', user_id)

        return render_template('myaccount.html', 
                            org_name=org_name, pending_reservations_info=pending_reservations_info, 
                               approved_reservations_info=approved_reservations_info
                            )
    
                            

    return app