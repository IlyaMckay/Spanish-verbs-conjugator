import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = current_dir[:current_dir.rfind('\\')]
sys.path.append(parent_dir)


import bisect
from time import sleep
from flask import current_app
from tinydb import TinyDB, Query
from app.conjugate import Conjugador
from app import app

def init_db():
    pass

def normalize_word(word):
    """
    Normalize the given word to its standard form by replacing special characters.
    
    Args:
        word (str): The word to normalize.

    Returns:
        str: The normalized word.
    """
    return word.lower().replace('í', 'i').replace('ñ', 'n').replace('ó', 'o').replace('ú', 'u')

def find_in_sorted_list(sorted_list, item):
    """
    Finds the index of an item in a sorted list using binary search.

    Args:
        sorted_list (list): A list sorted in ascending order.
        item: The item to search for.

    Returns:
        int: The index of the item if found, otherwise -1.
    """
    index = bisect.bisect_left(sorted_list, item)
    if index < len(sorted_list) and sorted_list[index] == item:
        return index
    return -1

def populate_db(verb):
    """
    Adds a verb to the TinyDB database if it does not already exist.

    Args:
        verb (str): The infinitive form of the verb to be added.
    """
    db_path = app.config['DATABASE']
    db = TinyDB(db_path)
    verbs_table = db.table('verbs')

    conjugate = Conjugador(verb)
    verb = conjugate.infinitivo.strip()
    final_dict = conjugate.final_dictionary()

    new_entry = {'verb': verb, 'conjugations': final_dict}

    sorted_entries = sorted(verbs_table.all(), key=lambda x: x['verb'])

    keys = [entry['verb'] for entry in sorted_entries]
    position = find_in_sorted_list(keys, new_entry['verb'])

    if position != -1:
        print(f"Verb '{verb}' already exists in the database.")
        return

    verbs_table.insert(new_entry)
    print(f"Verb '{verb}' has been added to the database.")


def get_verb(verb):
    """
    Retrieves a verb entry from the TinyDB database by first checking the exact match,
    and if not found, normalizing the keys in the database and trying again.

    Args:
        verb (str): The infinitive form of the verb to retrieve.

    Returns:
        dict or None: The verb entry if found, else None.
    """
    db_path = app.config['DATABASE']
    db = TinyDB(db_path)
    verbs_table = db.table('verbs')

    verb_entry = verbs_table.get(Query().verb == verb)
    
    if verb_entry:
        return verb_entry

    sorted_entries = sorted(verbs_table.all(), key=lambda x: normalize_word(x['verb']))
    normalized_verb = normalize_word(verb)
    normalized_keys = [normalize_word(entry['verb']) for entry in sorted_entries]
    position = find_in_sorted_list(normalized_keys, normalized_verb)

    if position != -1:
        return sorted_entries[position]

    return None


def truncate_all_tables():
    """
    Deletes all records from all tables in the TinyDB database.
    """
    db_path = app.config['DATABASE']
    db = TinyDB(db_path)

    for table_name in db.tables():
        db.table(table_name).truncate()


def show_first_five_records():
    """
    Prints the first five records from each table in the TinyDB database.
    """
    db_path = app.config['DATABASE']
    db = TinyDB(db_path)

    for table_name in db.tables():
        print(f"Records in table '{table_name}':")
        table = db.table(table_name)
        records = table.all()

        for record in records[:5]:
            print(record)
        print()