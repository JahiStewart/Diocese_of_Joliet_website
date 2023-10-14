import sqlite3

import click # command line scripts
from flask import current_app, g

# g is a special object unique to each request used to store data that can be accessed by multiple functions

def get_db():
    if 'db' not in g:
        # connect to database via file pointed at by 'DATABASE'
        g.db = sqlite3.connect(
            # special object that points to the Flask application handling the request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return rows that behave like dicts (allows access by column name)
        g.db.row_factory = sqlite3.Row

    return g.db

# closes connection to db
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # returns db connection
    db = get_db()
    
    # open file relative to flaskr package
    with current_app.open_resource('schema.sql') as f:
        # execute script inside 'schema.sql' (clear and create tables)
        db.executescript(f.read().decode('utf8'))

# Command line script to init database
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database')

# register app
def init_app(app):
    # call function after returning response
    app.teardown_appcontext(close_db)
    # adds new command that can be called with the 'flask' command
    app.cli.add_command(init_db_command)