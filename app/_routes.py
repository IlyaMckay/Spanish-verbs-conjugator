from flask import render_template, request, abort
from app import app
from app.conjugate import Conjugador
from app.populate_db import populate_db, get_verb
import re

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message=error.description), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message=error.description), 500

@app.route('/result', methods=['POST'])
def result():
    verb = request.form['verb']
    region = request.form['region']

    REGIONS = {
        'argentina': ['tú', 'vosotros, vosotras'],
        'espana': ['vos'],
        'mexico': ['vos', 'vosotros, vosotras']
    }

    if not re.match(r'^[a-zñáéíóúü]+$', verb, re.IGNORECASE):
        abort(400, description="Invalid word. Please enter a valid Spanish verb.")

    try:
        existing_entry = get_verb(verb)
    except Exception as e:
        abort(500, description="An error occurred while retrieving the verb.")

    if existing_entry:
        conjugations = existing_entry['conjugations']
        conjugations = Conjugador.filter_conjugations(conjugations, REGIONS.get(region, []))
        return render_template('result.html', verb=existing_entry['verb'], conjugations=conjugations)
    else:
        try:
            conjugador = Conjugador(verb)
            new_conjugations = conjugador.final_dictionary()
            filtered_conjugations = Conjugador.filter_conjugations(new_conjugations, REGIONS.get(region, []))
            
            populate_db(conjugador.infinitivo)
            
            return render_template('result.html', verb=conjugador.infinitivo, conjugations=filtered_conjugations)
        except RuntimeError as e:
            abort(500, description="An error occurred during conjugation.")
        except ValueError as e:
            abort(400, description=f"Invalid verb. Please enter a valid Spanish verb.")
        except Exception as e:
            abort(500, description=f"An unexpected error occurred: {e}")
