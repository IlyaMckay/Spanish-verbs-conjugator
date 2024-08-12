from flask import Flask, g
import os
from tinydb import TinyDB

app = Flask(__name__)

# Initialize the path to the database
db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, 'verbs.json')
app.config['DATABASE'] = db_path


def get_db():
    """
    Retrieve the TinyDB database instance.

    If the database instance does not exist in the application context,
    it creates a new TinyDB instance and assigns it to the application context.

    Returns:
        TinyDB: The TinyDB instance for the database.
    """
    if not hasattr(g, '_database'):
        g._database = TinyDB(app.config['DATABASE'])
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    """
    Close the TinyDB database connection at the end of the application context.

    This function is called when the application context is torn down,
    ensuring that the database connection is properly closed.

    Args:
        exception (Exception): The exception that caused the teardown, if any.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from app import routes
