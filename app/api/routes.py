import os

from app import app
from app.conjugate import Conjugador
from app.srv.verb import get_conjugations
from app.utils.form import form
from tomli import load

from flask import render_template, request

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
desc_file = os.path.join(parent_dir, 'resources', 'description.toml')


with open(desc_file, 'rb') as f:
    data = load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
@form.params(form=lambda: request.form, validators={"verb": Conjugador.is_spanish_verb})
def result(verb, region):
    verb_info, conjugations = get_conjugations(verb, region)
    return render_template('result.html', verb=verb_info, conjugations=conjugations, 
                                          description=data, region=region)
