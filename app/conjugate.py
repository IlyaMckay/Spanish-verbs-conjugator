import re
import string

from app.dao.http_request import get_site


class Conjugador:
    """
    A class used to parse and conjugate Spanish verbs.
    """
    REGIONS = {
        'argentina': ['tú', 'vosotros, vosotras'],
        'espana': ['vos'],
        'mexico': ['vos', 'vosotros, vosotras']
    }

    ESTAR = {
        'Indicativo': {
            'Presente': {'Yo': 'Estoy', 'Tú': 'Estás', 'Vos': 'Estás', 'Él, Ella, Usted': 'Está', 'Nosotros, Nosotras': 'Estamos', 'Vosotros, Vosotras': 'Estáis', 'Ellos, Ellas, Ustedes': 'Están'},
            'Imperfecto': {'Yo': 'Estaba', 'Tú': 'Estabas', 'Vos': 'Estabas', 'Él, Ella, Usted': 'Estaba', 'Nosotros, Nosotras': 'Estábamos', 'Vosotros, Vosotras': 'Estabais', 'Ellos, Ellas, Ustedes': 'Estaban'}
        },
        'Formas compuestas comunes': {
            'Pretérito perfecto': {'Yo': 'He estado', 'Tú': 'Has estado', 'Vos': 'Has estado', 'Él, Ella, Usted': 'Ha estado', 'Nosotros, Nosotras': 'Hemos estado', 'Vosotros, Vosotras': 'Habéis estado', 'Ellos, Ellas, Ustedes': 'Han estado'},
            'Pluscuamperfecto': {'Yo': 'Había estado', 'Tú': 'Habías estado', 'Vos': 'Habías estado', 'Él, Ella, Usted': 'Había estado', 'Nosotros, Nosotras': 'Habíamos estado', 'Vosotros, Vosotras': 'Habíais estado', 'Ellos, Ellas, Ustedes': 'Habían estado'}
        }
    }

    IR = {
        'Indicativo': {
            'Presente': {'Yo': 'Voy', 'Tú': 'Vas', 'Vos': 'Vas', 'Él, Ella, Usted': 'Va', 'Nosotros, Nosotras': 'Vamos', 'Vosotros, Vosotras': 'Vais', 'Ellos, Ellas, Ustedes': 'Van'},
            'Imperfecto': {'Yo': 'Iba', 'Tú': 'Ibas', 'Vos': 'Ibas', 'Él, Ella, Usted': 'Iba', 'Nosotros, Nosotras': 'Íbamos', 'Vosotros, Vosotras': 'Ibais', 'Ellos, Ellas, Ustedes': 'Iban'}
        }
    }

    DEBER = {
        'Indicativo': {
            'Presente': {'Yo': 'Debo', 'Tú': 'Debes', 'Vos': 'Debés', 'Él, Ella, Usted': 'Debe', 'Nosotros, Nosotras': 'Debemos', 'Vosotros, Vosotras': 'Debéis', 'Ellos, Ellas, Ustedes': 'Deben'},
            'Condicional': {'Yo': 'Debería', 'Tú': 'Deberías', 'Vos': 'Deberías', 'Él, Ella, Usted': 'Debería', 'Nosotros, Nosotras': 'Deberíamos', 'Vosotros, Vosotras': 'Deberíais', 'Ellos, Ellas, Ustedes': 'Deberían'}
        }
    }

    PODER = {
        'Indicativo': {
            'Presente': {'Yo': 'Puedo', 'Tú': 'Puedes', 'Vos': 'Podés', 'Él, Ella, Usted': 'Puede', 'Nosotros, Nosotras': 'Podemos', 'Vosotros, Vosotras': 'Podéis', 'Ellos, Ellas, Ustedes': 'Pueden'},
            'Condicional': {'Yo': 'Podría', 'Tú': 'Podrías', 'Vos': 'Podrías', 'Él, Ella, Usted': 'Podría', 'Nosotros, Nosotras': 'Podríamos', 'Vosotros, Vosotras': 'Podríais', 'Ellos, Ellas, Ustedes': 'Podrían'}
        }
    }

    def __init__(self, verb):
        """
        Initialize the Conjugate object for a given verb.

        :param verb: The verb to be conjugated.
        """
        self.verb = verb.strip()
        self.url = f'https://www.wordreference.com/conj/esverbs.aspx?v={self.verb}'
        self.parsed_html = get_site(self)
        self.parsed_igp = self.parse_infinitivo_gerundio_participio()
        self.infinitivo, self.gerundio, self.participio = self.process_infinitivo_gerundio_participio()
        self.parsed_dictionary = self.scrape_spanish_conjugations()
        self.new_dictionary = self.new_conjugations()
        self.exceptions = [
            'haber', 'costar', 'valer', 'doler', 'dolerse', 'gustar', 'interesar', 'encantar', 'desagradar', 'poder', 
            'deber', 'holgar', 'holgarse', 'urgir', 'atañer', 'acaecer', 'ocurrir', 'ocurrirse', 'acontecer', 'incumbir'
        ]

    def parse_infinitivo_gerundio_participio(self):
        """
        Extract the table containing verb conjugations from the HTML page,
        find the row with infinitive, gerund, and participle forms,
        and return them as a list.

        :return: A list containing the infinitive, gerund, and participle forms.
        """
        table = self.parsed_html.find('table', id='conjtable')

        if not table:
            return None

        row = table.find('tr', id='cheader')
        if not row:
            return None

        tds = row.find_all('td')
        if len(tds) < 2:
            return None

        content = tds[1].get_text(separator=' ').split()

        return content

    def process_infinitivo_gerundio_participio(self):
        """
        Process the list obtained from parse_infinitivo_gerundio_participio,
        clean and adjust the data, and return the infinitive, gerund,
        and participle forms.

        :return: A tuple containing the infinitive, gerund, and participle forms.
        """
        if self.parsed_igp is None:
            raise ValueError("parsed_igp is None. Please ensure that parse_infinitivo_gerundio_participio() has been called.")

        clear_content = [item.strip(string.punctuation) for item in self.parsed_igp if item.strip(string.punctuation).isalpha()]

        if not clear_content:
            raise ValueError("No valid items found in parsed_igp.")

        infinitivo = clear_content[0]

        if not infinitivo.endswith('se'):
            if not clear_content[1].endswith('ndo'):
                clear_content[1] += clear_content.pop(2)

            if len(clear_content) >= 4:
                if len(clear_content) == 4 and clear_content[-1].endswith('se'):
                    clear_content

                if ('cho' in clear_content[2] or
                    'cho' in clear_content[3] or
                    'uest' in clear_content[2] or
                    'uest' in clear_content[3] or
                    'ído' in clear_content[3] or
                    'isto' in clear_content[3]):
                    clear_content[2] += clear_content.pop(3)
        else:
            if not clear_content[1].endswith('ndose'):
                if not clear_content[2].endswith('ndose') and clear_content[3].endswith('ndose'):
                    clear_content.pop(1)
                    clear_content[1] += clear_content.pop(2)
                if clear_content[2].endswith('ndose'):
                    clear_content.pop(1)
                else:
                    if not clear_content[2].endswith('ndose'):
                        clear_content[1] += clear_content.pop(2)
                    else:
                        clear_content

                if clear_content[1].endswith('ndo') and not clear_content[2].endswith('ndose'):
                    clear_content.pop(1)
                    clear_content[1] += clear_content.pop(2)

            if len(clear_content) >= 4:
                if ('ndose' in clear_content[3] or
                    'cho' in clear_content[3] or
                    'uest' in clear_content[2] or
                    'isto' in clear_content[3] or
                    'ído' in clear_content[3]):
                    clear_content[2] += clear_content.pop(3)

        if self.verb.lower() in ['freir', 'freirse']:
            clear_content[2] = clear_content[2] + ' ' + clear_content.pop(
                3) + ' ' + clear_content.pop(3) + clear_content.pop(3)
        elif self.verb.lower() in ['imprimir', 'proveer', 'proveerse', 'desproveer', 'sofreir', 'sofreirse']:
            clear_content[2] = clear_content[2] + ' ' + clear_content.pop(3) + ' ' + clear_content.pop(3)

        if 'ndose' in clear_content[2]:
            infinitivo, gerundio, participio = clear_content[0], clear_content[1], clear_content[3]

        else:
            infinitivo, gerundio, participio = clear_content[:3]

        return infinitivo, gerundio, participio

    def remove_after_last_o(self, header, tense, input_string):
        """
        Remove text after the last occurrence of 'o' in the input string for certain verb exceptions,
        unless specific conditions related to the header and tense are met.

        :param header: The header indicating the type of conjugation.
        :param tense: The tense of the conjugation.
        :param input_string: The conjugation string to process.
        :return: The processed conjugation string with text removed after the last 'o'.
        """
        exceptions = [
            'despertar', 'despertarse', 'convertir', 'convertirse', 'bendecir', 'bendecirse',
            'maldecir', 'nacer', 'pagar', 'atender', 'concluir', 'poseer', 'poseerse', 'soltar', 'soltarse'
        ]

        if ' o nado o nato' in input_string:
            input_string = input_string.split(' o nado o nato')[0]
            return input_string

        if self.verb.lower() in exceptions:
            if ' o ' in input_string and header != 'Subjuntivo' and tense != 'Imperfecto':
                return input_string[:input_string.rfind(' o ')]

        return input_string

    def scrape_spanish_conjugations(self):
        """
        Scrape Spanish conjugations from HTML tables, extracting and processing the conjugation data
        based on pronouns and tenses. Cleans and formats the data, handling special cases.

        :return: A dictionary containing the conjugation data organized by header, tense, and pronouns.
        """
        tables = self.parsed_html.find_all('table', class_='neoConj')
        conjugations = {}

        for table in tables:
            header = table.find_previous_sibling('h4').get_text(strip=True)
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                pronouns = row.find_all('th', scope="row")

                if not pronouns or not cells:
                    continue

                tense = row.find_previous('th', colspan='2').get_text().split('ⓘ')[0].strip().capitalize()

                if header not in conjugations:
                    conjugations[header] = {}
                if tense not in conjugations[header]:
                    conjugations[header][tense] = {}

                for pronoun, cell in zip(pronouns, cells):
                    pronoun_text = pronoun.get_text().strip()

                    if not pronoun_text:
                        pronoun_text = 'Yo'
                    elif pronoun_text.startswith('(') and pronoun_text.endswith(')'):
                        pronoun_text = pronoun_text[1:-1].strip()

                    pronoun_text = pronoun_text.capitalize()

                    if ',' in pronoun_text:
                        pronoun_words = [word.strip().capitalize()
                                         for word in pronoun_text.split(',')]
                        pronoun_text = ', '.join(pronoun_words)
                    else:
                        pronoun_text = pronoun_text.capitalize()

                    conjugation = cell.get_text().capitalize()

                    if conjugation.startswith('¡'):
                        conjugation = '¡' + conjugation[1:].capitalize()

                    if '–' in conjugation:
                        conjugation = 'N/A'

                    if ', ' in conjugation:
                        conjugation = conjugation.split(', ')[0]

                    if pronoun_text == 'Vos':
                        if ',' in conjugation:
                            conjugation = conjugation.split(', ')[0]
                        if conjugation.startswith('¡') and tense == 'Negativo':
                            conjugation = '¡' + \
                                conjugation[1:].split(', ')[0].capitalize() + '!'

                    conjugation = self.remove_after_last_o(header, tense, conjugation)

                    if pronoun_text in conjugations[header][tense]:
                        continue

                    conjugations[header][tense][pronoun_text] = conjugation

        conjugations = self.reorder_pronouns(conjugations)

        return conjugations

    def reorder_pronouns(self, conjugations):
        """
        Reorder pronouns in the conjugation dictionary, ensuring 'Vos' is placed correctly in the sequence.
        Adjusts the order of pronouns and returns the updated conjugation dictionary.

        :param conjugations: A dictionary containing conjugation data.
        :return: The updated dictionary with reordered pronouns.
        """
        for header, tenses in conjugations.items():
            for tense, pronouns in tenses.items():
                if 'Vos' in pronouns:
                    ordered_pronouns = {k: pronouns[k] for k in pronouns if k != 'Vos'}

                    ordered_keys = list(ordered_pronouns.keys())

                    ordered_keys.insert(2, 'Vos')

                    conjugations[header][tense] = {k: pronouns[k] for k in ordered_keys}

        return conjugations

    @staticmethod
    def replace_gerundio_suffix(gerundio, pronoun):
        """
        Replace the suffix of the gerundio form based on the given pronoun.

        :param gerundio: The gerundio form of the verb.
        :param pronoun: The pronoun associated with the conjugation.
        :return: The gerundio form with the appropriate suffix replaced.
        """
        replacements = {
            'Yo': 'ndome',
            'Tú': 'ndote',
            'Vos': 'ndote',
            'Nosotros, Nosotras': 'ndonos',
            'Vosotros, Vosotras': 'ndoos'
        }

        if gerundio.endswith('ndose'):
            if pronoun in replacements:
                gerundio = gerundio[:-5] + replacements[pronoun]

        return gerundio

    @staticmethod
    def replace_infinitivo_suffix(infinitivo, pronoun):
        """
        Replace the suffix of the infinitivo form based on the given pronoun.

        :param infinitivo: The infinitivo form of the verb.
        :param pronoun: The pronoun associated with the conjugation.
        :return: The infinitivo form with the appropriate suffix replaced.
        """
        replacements = {
            'Yo': 'rme',
            'Tú': 'rte',
            'Vos': 'rte',
            'Nosotros, Nosotras': 'rnos',
            'Vosotros, Vosotras': 'ros'
        }

        if infinitivo.endswith('rse'):
            if pronoun in replacements:
                infinitivo = infinitivo[:-3] + replacements[pronoun]

        return infinitivo

    def change_haber_form(self, pronoun):
        """
        Change the form of 'haber' based on the given pronoun and the verb's infinitive form.

        :param pronoun: The pronoun associated with the conjugation.
        :return: The form of 'haber' corresponding to the given pronoun.
        """
        if not self.infinitivo.endswith('se'):
            return 'haber'
        else:
            replacements = {
                'Yo': 'haberme',
                'Tú': 'haberte',
                'Vos': 'haberte',
                'Él, Ella, Usted': 'haberse',
                'Nosotros, Nosotras': 'habernos',
                'Vosotros, Vosotras': 'haberos',
                'Ellos, Ellas, Ustedes': 'haberse'
            }
            return replacements.get(pronoun, 'haber')

    def add_new_conjugations_estar(self, conjugations, tense_name, tense_data, gerundio):
        """
        Add new conjugations for the verb 'estar' to the conjugation dictionary.

        :param conjugations: The dictionary of conjugations to update.
        :param tense_name: The name of the tense for which to add conjugations.
        :param tense_data: The data containing the conjugations for the specified tense.
        :param gerundio: The gerundio form of the verb.
        """
        for pronoun, conjugation in tense_data.items():
            gerundio_form = self.replace_gerundio_suffix(gerundio, pronoun)
            conjugations[pronoun] = f"{conjugation} {gerundio_form}"

    def add_new_conjugations_ir_infinitivo(self, conjugations, tense_name, tense_data, infinitivo):
        """
        Add new conjugations for the verb 'ir' with infinitivo to the conjugation dictionary.

        :param conjugations: The dictionary of conjugations to update.
        :param tense_name: The name of the tense for which to add conjugations.
        :param tense_data: The data containing the conjugations for the specified tense.
        :param infinitivo: The infinitivo form of the verb.
        """
        for pronoun, conjugation in tense_data.items():
            infinitivo_form = self.replace_infinitivo_suffix(infinitivo, pronoun)
            conjugations[pronoun] = f"{conjugation} a {infinitivo_form}"

    def add_new_conjugations_ir_participio(self, conjugations, tense_name, tense_data, participio):
        """
        Add new conjugations for the verb 'ir' with participio to the conjugation dictionary.

        :param conjugations: The dictionary of conjugations to update.
        :param tense_name: The name of the tense for which to add conjugations.
        :param tense_data: The data containing the conjugations for the specified tense.
        :param participio: The participio form of the verb.
        """
        
        for pronoun, conjugation in tense_data.items():
            haber_form = self.change_haber_form(pronoun)
            if self.verb.endswith('se'):
                conjugations[pronoun] = \
                    f"{conjugation} a {haber_form} {participio}"
            else:
                conjugations[pronoun] = f"{conjugation} a haber {participio}"

    def add_new_conjugations_deber_poder_participio(self, conjugations, tense_name, tense_data, participio):
        """
        Add new conjugations for the verbs 'deber' and 'poder' with participio to the conjugation dictionary.

        :param conjugations: The dictionary of conjugations to update.
        :param tense_name: The name of the tense for which to add conjugations.
        :param tense_data: The data containing the conjugations for the specified tense.
        :param participio: The participio form of the verb.
        """
        
        for pronoun, conjugation in tense_data.items():
            haber_form = self.change_haber_form(pronoun)
            if self.verb.endswith('se'):
                conjugations[pronoun] = \
                    f"{conjugation} {haber_form} {participio}"
            else:
                conjugations[pronoun] = f"{conjugation} haber {participio}"

    def new_conjugations(self):
        """
        Generate new conjugations for various tenses and forms of the verb and return them.

        :return: A dictionary of new conjugations organized by tense and pronoun.
        """
        infinitivo = self.infinitivo
        gerundio = self.gerundio
        participio = self.participio

        conjugations = {
            'Presente con Estar': {},
            'Preterito perfecto compuestas comunes con Estar': {},
            'Pasado continuo': {},
            'Pluscuamperfecto continuo': {},
            'Intencion interrumpida': {},
            'Futuro con Ir a': {},
            'Futuro perfecto con Ir a': {},
            'Podria haber': {},
            'Deberia haber': {},
            'Puede haber': {},
            'Debe haber': {}
        }

        self.add_new_conjugations_estar(
            conjugations['Presente con Estar'], 'Presente con Estar', self.__class__.ESTAR['Indicativo']['Presente'], gerundio)
        self.add_new_conjugations_estar(conjugations['Preterito perfecto compuestas comunes con Estar'],
                                        'Preterito perfecto compuestas comunes con Estar', self.__class__.ESTAR['Formas compuestas comunes']['Pretérito perfecto'], gerundio)
        self.add_new_conjugations_estar(
            conjugations['Pasado continuo'], 'Pasado continuo', self.__class__.ESTAR['Indicativo']['Imperfecto'], gerundio)
        self.add_new_conjugations_estar(conjugations['Pluscuamperfecto continuo'], 'Pluscuamperfecto continuo',
                                        self.__class__.ESTAR['Formas compuestas comunes']['Pluscuamperfecto'], gerundio)
        self.add_new_conjugations_ir_infinitivo(
            conjugations['Intencion interrumpida'], 'Intencion interrumpida', self.__class__.IR['Indicativo']['Imperfecto'], infinitivo)
        self.add_new_conjugations_ir_infinitivo(
            conjugations['Futuro con Ir a'], 'Futuro con Ir a', self.__class__.IR['Indicativo']['Presente'], infinitivo)
        self.add_new_conjugations_ir_participio(
            conjugations['Futuro perfecto con Ir a'], 'Futuro perfecto con Ir a', self.__class__.IR['Indicativo']['Presente'], participio)
        self.add_new_conjugations_deber_poder_participio(
            conjugations['Podria haber'], 'Podria haber', self.__class__.PODER['Indicativo']['Condicional'], participio)
        self.add_new_conjugations_deber_poder_participio(
            conjugations['Deberia haber'], 'Deberia haber', self.__class__.DEBER['Indicativo']['Condicional'], participio)
        self.add_new_conjugations_deber_poder_participio(
            conjugations['Puede haber'], 'Puede haber', self.__class__.PODER['Indicativo']['Presente'], participio)
        self.add_new_conjugations_deber_poder_participio(
            conjugations['Debe haber'], 'Debe haber', self.__class__.DEBER['Indicativo']['Presente'], participio)

        return conjugations

    def change_pronouns(self, final_dict, singular_pronoun, plural_pronoun=None):
        """
        Changes pronouns in the final_dict based on the provided singular and optional plural pronouns.
        """
        for tense in list(final_dict.keys()):
            filtered_pronouns = {}
            for pronoun, conjugation in final_dict[tense].items():
                if pronoun == 'Él, Ella, Usted':
                    filtered_pronouns[singular_pronoun] = conjugation
                if plural_pronoun and pronoun == 'Ellos, Ellas, Ustedes':
                    filtered_pronouns[plural_pronoun] = conjugation
            if filtered_pronouns:
                final_dict[tense] = filtered_pronouns
            else:
                del final_dict[tense]

    def filter_impersonal_verbs(self, final_dict):
        self.change_pronouns(final_dict, singular_pronoun='Impersonal')

    def filter_singular_plural_verbs(self, final_dict):
        self.change_pronouns(final_dict, singular_pronoun='Singular', plural_pronoun='Plural')

    def final_dictionary(self):
        """
        Generate a comprehensive dictionary of verb conjugations across various tenses.

        This method compiles conjugation forms for a wide range of tenses based on predefined 
        rules and exceptions. It processes tenses from different categories including 
        indicative, subjunctive, and imperative moods, and adjusts the entries for specific 
        verbs such as 'haber', 'llover', and others.

        :return: A dictionary with conjugations organized by tense and pronoun.
        """
        final_dict = {
            'Presente indicativo': {}, 'Presente con Estar': {}, 'Preterito perfecto compuestas comunes': {},
            'Preterito perfecto compuestas comunes con Estar': {}, 'Preterito indicativo': {}, 'Imperfecto indicativo': {},
            'Pasado continuo': {}, 'Pluscuamperfecto compuestas comunes': {}, 'Preterito anterior indicativo': {},
            'Pluscuamperfecto continuo': {}, 'Intencion interrumpida': {}, 'Imperativo afirmativo': {}, 'Imperativo negativo': {},
            'Cohortativo afirmativo': {}, 'Cohortativo negativo': {}, 'Futuro con Ir a': {}, 'Futuro indicativo': {},
            'Preterito perfecto compuestos del subjuntivo': {}, 'Futuro perfecto compuestas comunes': {},
            'Futuro perfecto con Ir a': {}, 'Presente subjuntivo': {}, 'Imperfecto subjuntivo': {}, 'Futuro subjuntivo': {},
            'Pluscuamperfecto compuestos del subjuntivo': {}, 'Condicional indicativo': {}, 'Condicional perfecto compuestas comunes': {},
            'Podria haber': {}, 'Deberia haber': {}, 'Puede haber': {}, 'Debe haber': {}
        }

        for tense in list(final_dict.keys()):

            if tense == 'Presente indicativo':
                if self.verb.lower() == 'haber':
                    final_dict[tense] = {}
                    for pronoun, conjugation in self.parsed_dictionary['Indicativo']['Presente'].items():
                        if pronoun == 'Él, Ella, Usted':
                            parts = conjugation.split(', ')[1].split(': ')
                            value = parts[1].capitalize()
                            final_dict[tense][pronoun] = value
                else:
                    final_dict[tense] = self.parsed_dictionary['Indicativo']['Presente']
            if tense == 'Presente con Estar':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Preterito perfecto compuestas comunes':
                final_dict[tense] = self.parsed_dictionary['Formas compuestas comunes']['Pretérito perfecto']
            if tense == 'Preterito perfecto compuestas comunes con Estar':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Preterito indicativo':
                final_dict[tense] = self.parsed_dictionary['Indicativo']['Pretérito']
            if tense == 'Imperfecto indicativo':
                final_dict[tense] = self.parsed_dictionary['Indicativo']['Imperfecto']
            if tense == 'Pasado continuo':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Pluscuamperfecto compuestas comunes':
                final_dict[tense] = self.parsed_dictionary['Formas compuestas comunes']['Pluscuamperfecto']
            if tense == 'Preterito anterior indicativo':
                final_dict[tense] = self.parsed_dictionary['Indicativo']['Pretérito anterior']
            if tense == 'Pluscuamperfecto continuo':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Intencion interrumpida':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Imperativo afirmativo':
                if self.verb in self.exceptions:
                    del final_dict[tense]
                else:
                    final_dict[tense] = {
                        pronoun: '¡' + conjugation[1:].capitalize()
                        for pronoun, conjugation in self.parsed_dictionary['Imperativo']['Afirmativo'].items()
                        if pronoun not in ['Yo', 'Nosotros, Nosotras']
                    }
            if tense == 'Imperativo negativo':
                if self.verb in self.exceptions:
                    del final_dict[tense]
                else:
                    final_dict[tense] = {
                        pronoun: '¡' + conjugation[1:].capitalize()
                        for pronoun, conjugation in self.parsed_dictionary['Imperativo']['Negativo'].items()
                        if pronoun not in ['Yo', 'Nosotros, Nosotras']
                    }
            if tense == 'Cohortativo afirmativo':
                if self.verb in self.exceptions:
                    del final_dict[tense]
                else:
                    final_dict[tense] = {
                        pronoun: '¡' + conjugation[1:].capitalize()
                        for pronoun, conjugation in self.parsed_dictionary['Imperativo']['Afirmativo'].items()
                        if pronoun == 'Nosotros, Nosotras'
                    }
            if tense == 'Cohortativo negativo':
                if self.verb in self.exceptions:
                    del final_dict[tense]
                else:
                    if self.verb.endswith('se'):
                        final_dict[tense] = {
                            pronoun: '¡' + conjugation[1:].capitalize()
                            for pronoun, conjugation in self.parsed_dictionary['Imperativo']['Negativo'].items()
                            if pronoun == 'Nosotros, Nosotras'
                        }
                    else:
                        del final_dict[tense]
            if tense == 'Futuro con Ir a':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Futuro indicativo':
                final_dict[tense] = self.parsed_dictionary['Indicativo']['Futuro']
            if tense == 'Preterito perfecto compuestos del subjuntivo':
                final_dict[tense] = self.parsed_dictionary['Tiempos compuestos del subjuntivo']['Pretérito perfecto']
            if tense == 'Futuro perfecto compuestas comunes':
                final_dict[tense] = self.parsed_dictionary['Formas compuestas comunes']['Futuro perfecto']
            if tense == 'Futuro perfecto con Ir a':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Presente subjuntivo':
                final_dict[tense] = self.parsed_dictionary['Subjuntivo']['Presente']
            if tense == 'Imperfecto subjuntivo':
                final_dict[tense] = self.parsed_dictionary['Subjuntivo']['Imperfecto']
            if tense == 'Futuro subjuntivo':
                final_dict[tense] = self.parsed_dictionary['Subjuntivo']['Futuro']
            if tense == 'Pluscuamperfecto compuestos del subjuntivo':
                final_dict[tense] = self.parsed_dictionary['Tiempos compuestos del subjuntivo']['Pluscuamperfecto']
            if tense == 'Condicional indicativo':
                final_dict[tense] = self.parsed_dictionary['Indicativo']['Condicional']
            if tense == 'Condicional perfecto compuestas comunes':
                final_dict[tense] = self.parsed_dictionary['Formas compuestas comunes']['Condicional perfecto']
            if tense == 'Podria haber':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Deberia haber':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Puede haber':
                final_dict[tense] = self.new_dictionary[tense]
            if tense == 'Debe haber':
                final_dict[tense] = self.new_dictionary[tense]

        if self.verb.lower() in ['haber', 'llover', 'lloviznar', 'diluviar', 'nevar', 'granizar']:
            self.filter_impersonal_verbs(final_dict)

        if self.verb.lower() in ['doler', 'interesar', 'encantar', 'desagradar', 'holgar', 'urgir', 'ocurrir', 
                                'ocurrirse', 'incumbir', 'acontecer', 'acaecer', 'atañer']:
            self.filter_singular_plural_verbs(final_dict)

        return final_dict


    @staticmethod
    def filter_conjugations(conjugations, accents):
        """
        Filters conjugations based on specified pronoun variants (accents).

        This function removes conjugations associated with pronouns that are found in 
        the list of accents. It returns a dictionary of conjugations, excluding 
        those pronouns that match the specified accents.

        :param conjugations: A dictionary of conjugations, where the keys are tenses 
                            and the values are dictionaries of pronouns and their conjugated forms.
        :param accents: A list of pronouns to be excluded from the conjugations.
        :return: A filtered dictionary of conjugations excluding the specified accents.
        """
        
        filtered_conjugations = {}

        for tense, pronouns in conjugations.items():
            filtered_conjugations[tense] = {}
            for pronoun, conjugation in pronouns.items():
                if pronoun.lower() not in accents:
                    filtered_conjugations[tense][pronoun] = conjugation

        return filtered_conjugations

    @staticmethod
    def is_spanish_verb(word):
        if not re.match(r'^[a-zñáéíóúü]+$', word, re.IGNORECASE):
            raise ValueError("К сожалению, мы не нашли такой глагол. Пожалуйста, проверьте корректность ввода.")
