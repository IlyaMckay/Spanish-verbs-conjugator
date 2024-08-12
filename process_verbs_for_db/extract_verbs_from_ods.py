import os
import pyexcel_ods3


def clean_data(data):
    """
    Clean data: remove the unnecessary characters, trim spaces
    """
    cleaned = data.replace('(n)', 'n').split(' (')[0].strip()
    return cleaned


def is_valid_verb(data):
    """
    Check if the string is a valid verb
    """
    return len(data) > 1 and 'irregular' not in data


def extract_verbs_from_ods(ods_path):
    """
    Extract verbs from a ODS
    """
    verbs = []

    data = pyexcel_ods3.get_data(ods_path)

    for sheet, rows in data.items():
        for row in rows:
            if len(row) > 0:
                cleaned_data = clean_data(row[0])
                if is_valid_verb(cleaned_data):
                    verbs.append(cleaned_data)

    return verbs


ods_path = f"{os.path.dirname(os.path.abspath(__file__)) + '\\verbs_lists\\irregulares.ods'}"

verbs = extract_verbs_from_ods(ods_path)
