import os
import pdfplumber


def clean_data(data):
    """
    Clean data: remove the bullet point and unnecessary characters, trim spaces
    """
    cleaned = data.replace('• ', '').split(' (')[0].split(' [')[0].strip()
    return cleaned


def is_valid_verb(data):
    """
    Check if the string is a valid verb
    """
    return len(data) > 1 and ' ' not in data


def extract_verbs_from_pdf(pdf_path):
    """
    Extract verbs from a PDF
    """
    verbs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for lists in table:
                    for data in lists:
                        if '•' in data:
                            cleaned_data = clean_data(data)
                            if is_valid_verb(cleaned_data):
                                verbs.append(cleaned_data)

    return verbs


pdf_path = f"{os.path.dirname(os.path.abspath(__file__)) + '\\verbs_lists\\1K-Spanish-Verbs.pdf'}"

verbs = extract_verbs_from_pdf(pdf_path)
