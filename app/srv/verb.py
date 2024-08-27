from app.conjugate import Conjugador
from app.dao.db import get_verb, populate_db

def get_conjugations(verb, region):
    existing_entry = get_verb(verb)
    if existing_entry:
        conjugations = existing_entry['conjugations']
        conjugations = Conjugador.filter_conjugations(conjugations, Conjugador.REGIONS.get(region, []))
        return (existing_entry['verb'], conjugations)
    else:
        conjugador = Conjugador(verb)
        new_conjugations = conjugador.final_dictionary()
        filtered_conjugations = Conjugador.filter_conjugations(new_conjugations, Conjugador.REGIONS.get(region, []))
        populate_db(conjugador.infinitivo)
        return (conjugador.infinitivo, filtered_conjugations)