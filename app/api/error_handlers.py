from app import app

from flask import render_template


@app.errorhandler(ValueError)
def validation_error(error):
    print(f"Validation Error: {error}")
    return render_template('error.html', error_message=str(error)), 400

@app.errorhandler(404)
def not_found_error(error):
    print(f"404 Error: {error}")
    return render_template('error.html', error_message=str(error)), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"500 Error: {error}")
    return render_template('error.html', error_message=str(error)), 500
