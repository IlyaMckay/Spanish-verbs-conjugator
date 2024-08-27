from flask import render_template, request
from app import app
from app.conjugate import Conjugador
from app.utils.form import form
from app.srv.verb import get_conjugations
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
@form.params(form=lambda: request.form, validators={"verb": Conjugador.is_spanish_verb})
def result(verb, region):
    verb_info, conjugations = get_conjugations(verb, region)
    return render_template('result.html', verb=verb_info, conjugations=conjugations)
