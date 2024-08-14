from bs4 import BeautifulSoup
import requests


class Conjugador:
    """
    A class used to parse and conjugate Spanish verbs.
    """
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
        self.parsed_html = self.get_site()
        self.parsed_igp = self.parse_infinitivo_gerundio_participio()
        self.infinitivo, self.gerundio, self.participio = self.process_infinitivo_gerundio_participio()
        self.parsed_dictionary = self.scrape_spanish_conjugations()
        self.new_dictionary = self.new_conjugations()
        self.exceptions = [
            'haber', 'costar', 'valer', 'doler', 'dolerse', 'gustar', 'interesar', 'encantar', 'desagradar'
        ]

    def get_site(self):
        """
        Send an HTTP request to the specified URL and return the parsed HTML content.

        :return: Parsed HTML content of the webpage.
        :raises RuntimeError: If the webpage could not be retrieved.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            parsed_html = BeautifulSoup(response.text, 'html.parser')

            return parsed_html
        else:
            raise RuntimeError("Failed to retrieve the webpage.")

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

        clear_content = [item for item in self.parsed_igp if item.isalpha()]

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

                    if pronoun_text == 'Vos':
                        if ',' in conjugation:
                            conjugation = conjugation.split(', ')[0]
                        if conjugation.startswith('¡') and tense == 'Negativo':
                            conjugation = '¡' + \
                                conjugation[1:].split(', ')[0].capitalize() + '!'

                    conjugation = self.remove_after_last_o(
                        header, tense, conjugation)

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
        replacements = {
            'Yo': 'o me',
            'Tú': 'o te',
            'Vos': 'o te',
            'Él, Ella, Usted': 'o se',
            'Nosotros, Nosotras': 'o nos',
            'Vosotros, Vosotras': 'u os',
            'Ellos, Ellas, Ustedes': 'o se'
        }
        for pronoun, conjugation in tense_data.items():
            haber_form = self.change_haber_form(pronoun)
            if self.verb.endswith('se'):
                conjugations[pronoun] = \
                    f"{conjugation} a {haber_form} {participio} {replacements[pronoun]} {conjugation.lower()} a haber {participio}"
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
        replacements = {
            'Yo': 'o me',
            'Tú': 'o te',
            'Vos': 'o te',
            'Él, Ella, Usted': 'o se',
            'Nosotros, Nosotras': 'o nos',
            'Vosotros, Vosotras': 'u os',
            'Ellos, Ellas, Ustedes': 'o se'
        }
        for pronoun, conjugation in tense_data.items():
            haber_form = self.change_haber_form(pronoun)
            if self.verb.endswith('se'):
                conjugations[pronoun] = \
                    f"{conjugation} {haber_form} {participio} {replacements[pronoun]} {conjugation.lower()} haber {participio}"
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
            for tense in list(final_dict.keys()):
                filtered_pronouns = {}
                for pronoun, conjugation in final_dict[tense].items():
                    if pronoun == 'Él, Ella, Usted':
                        filtered_pronouns['Impersonal'] = conjugation
                if filtered_pronouns:
                    final_dict[tense] = filtered_pronouns
                else:
                    del final_dict[tense]

        return final_dict

    


    @staticmethod
    def filter_conjugations(conjugations, accents):
        """
        Filter out conjugations based on specified accents.

        This method removes conjugations associated with pronouns that match any of the 
        specified accents. It returns a filtered dictionary of conjugations.

        :param conjugations: A dictionary of conjugations to be filtered.
        :param accents: A list of accents to be excluded from the conjugations.
        :return: A filtered dictionary of conjugations with specified accents removed.
        """
        esp_to_rus_dict = {
            'Presente indicativo': {
                '1: Настоящее время<br>2: Условие "если"': 
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Не для кроткосрочных процессов.<br>
                    <b style="color: #7891BF">Пример: </b>El niño no come pescado.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Ребёнок не ест рыбу (Никогда. Ему не нравится)<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Вероятное и возможное условие, в настоящем времени и в будущем.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в настоящем времени или в будущем.<br>
                    <b style="color: #7891BF">Пример: </b>Si <u>llueve</u> mañana, me quedaré en casa.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если завтра <u>будет</u> дождь, я останусь дома.'''
            },
            'Presente con Estar': {
                'Краткосрочный и/или постоянный процесс в настоящем времени':
                '''<b style="color: #7891BF">Использование: </b>
                    Факты и утверждения. Для кроткосрочных и постоянных процессов в настоящем времени.<br>
                    <b style="color: #7891BF">Пример: </b>Están durmiendo.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Они спят.'''
            },
            'Preterito perfecto compuestas comunes': {
                'Расширенное прошедшее время'
                '''<b style="color: #7891BF">Использование: </b>
                     Факты и утверждения. Продолжающееся действие / Может повторяться / Пока нет, но ещё возможно.<br>
                    <b style="color: #7891BF">Примеры: </b>Ha llovido todo el día.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Весь день шёл дождь (и всё ещё идёт).<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Me ha llamado cinco veces hoy.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Сегодня она звонила мне пять раз (и может позвонить снова).<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    No hemos tenido problemas con este ascensor.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    У нас (до сих пор) не было проблем с этим лифтом.'''
            },
            'Preterito perfecto compuestas comunes con Estar': {
                'Процесс за последнее время': 
                '''<b style="color: #7891BF">Использование: </b>
                    Факты и утверждения. Продолжающийся процесс за последнее время.<br>
                    <b style="color: #7891BF">Пример: </b>He estado viajando por tres semanas.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я путешествую уже три недели (и я всё ещё в пути).'''
            },
            'Preterito indicativo': {
                'Прошедшее время совершённого вида':
                '''<b style="color: #7891BF">Использование: </b>
                    Факты и утверждения. Описание целого, завершенного действия в прошлом.<br>
                    <b style="color: #7891BF">Пример: </b>Compré frutas ayer.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Вчера я купил фрукты.'''
            },
            'Imperfecto indicativo': {
                'Прошедшее время несовершённого вида':
                '''<b style="color: #7891BF">Использование: </b>
                    Факты и утверждения. Описание части действия или обычай в прошлом.<br>
                    <b style="color: #7891BF">Пример: </b>Yo <u>jugaba</u> en este parque cuando era niño.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я играл в этом парке когда был ребёнком.'''
            },
            'Pasado continuo': {
                'Процесс в прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Описание краткосрочного процесса, во время момента в прошлом.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени совершённого вида.<br>
                    <b style="color: #7891BF">Пример: </b>Estábamos comiendo cuando sonó la alarma.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Мы ели, когда сработала сигнализация.<br>'''
            },
            'Pluscuamperfecto compuestas comunes': {
                'Действие завершилось до другого момента в прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Действие завершилось до другого момента в прошлом.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени совершённого вида.<br>
                    <b style="color: #7891BF">Пример: </b>Ya habían inventado el teléfono cuando se popularizó la radio.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Телефон уже был изобретен, когда радио стало популярным.<br>'''
            },
            'Preterito anterior indicativo': {
                'Процесс завершился как условие для другого действия':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Условие завершилось и затем последовало другое действие ("После того как").<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени совершённого вида.<br>
                    <b style="color: #7891BF">Пример: </b>Cuando <u>hube terminado</u> el trabajo, me pagaron.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    (Только) После того, как я закончил работу, они мне заплатили.<br>'''
            },
            'Pluscuamperfecto continuo': {
                'Краткосрочный процесс до другого момента в прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Краткосрочный и постоянный процесс до другого момента в прошлом.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени совершённого вида.<br>
                    <b style="color: #7891BF">Пример: </b>Yo <u>había estado leyendo</u> sobre canguros cuando me ofrecieron viajar a Australia.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я читал (немного) о кенгуру (до того момента), когда мне предложили поехать в Австралию.<br>'''
            },
            'Intencion interrumpida': {
                '1: Прерванное намерение<br>2: Предсказание в прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Факты и утверждения. Прерванное намерение ("собирался").<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени.<br>
                    <b style="color: #7891BF">Пример: </b><u>Íbamos a comprar</u> una computadora nueva pero nos dijeron que era fácil reparar la vieja.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Мы собирались купить новый компьютер, но нам сказали, что было возможно отремонтировать старый.<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Предсказание в прошлом.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени.<br>
                    <b style="color: #7891BF">Пример: </b> Creíamos que <u>ibas a llegar</u> más tarde.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Мы думали, что ты <u>доберёшься</u> позже.'''
            },
            'Imperativo afirmativo': {
                'Утвердительное повелительное наклонение':
                '''<b style="color: #7891BF">Пример: </b>¡Miren qué lindo edificio!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Посмотрите, какое красивое здание!'''
            },
            'Imperativo negativo': {
                'Отрицательное повелительное наклонение':
                '''<b style="color: #7891BF">Пример: </b>¡No toques esos cables!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Не трогай эти кабели!'''
            },
            'Cohortativo afirmativo': {
                'Гортатив (утвердительный)':
                '''<b style="color: #7891BF">Использование: </b>
                    Призыв к действию с намерением участвовать в реализации желаемой ситуации ("Давайте сделаем!").<br>
                    <b style="color: #7891BF">Пример: </b>Hablemos mañana.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Давай поговорим завтра.'''
            },
            'Cohortativo negativo': {
                'Гортатив (отрицательный)':
                '''<b style="color: #7891BF">Использование: </b>
                    Призыв к бездействию с намерением говорящего самому участвовать в реализации желаемой ситуации ("Давайте не будем делать!").<br>
                    <b style="color: #7891BF">Пример: </b>No nos peleemos.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Давайте не будем спорить.'''
            },
            'Futuro con Ir a': {
                '1: Будущее время (наиболее распространённая форма)<br>2: Недоверие о настоящем времени или о будущем':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Обещания и предсказания. Будущее время (наиболее распространённая форма).<br>
                    <b style="color: #7891BF">Пример: </b>Voy a comprar frutas.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я куплю фрукты (Я собираюсь купить фрукты).<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Удивление, недоверие, неодобрение или замешательство о настоящем времени или о будущем.<br>
                    <b style="color: #7891BF">Примеры: </b>¿Cómo vas a hacer algo tan insensato?<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Как ты собираешься сделать что-то настолько безрассудное?
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    ¡Qué va a ser millonario! ¡Es mitómano!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Какой из него миллионер?! Он - лжец!'''
            },
            'Futuro indicativo': {
                '1: Будущее время (формальное)<br>2: Гипотеза о настоящем времени':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Обещания и предсказания. Будущее время (формальное).<br>
                    <b style="color: #7891BF">Пример: </b>Volveremos la semana que viene.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Мы вернёмся на следующей неделе.<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Задаваться вопросом, интересоваться или гипотеза о настоящем времени.<br>
                    <b style="color: #7891BF">Примеры: </b>No sabrá qué hacer.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Разве он может не знать, что делать?
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    ¿Estará triste?<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    (Я не понимаю, почему он ведёт себя так) Возможно, он грустный?'''
            },
            'Preterito perfecto compuestos del subjuntivo': {
                'Процесс будет завершён как условие для другого действя':
                '''<b style="color: #7891BF">Использование: </b>
                    Условие будет выполнено, после чего произойдет другое действие ("после того как").<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в будущем.
                    <b style="color: #7891BF">Пример: </b>Cuando <u>hayas terminado</u> el libro, entenderás el problema.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    После того, как закончишь книгу, ты (сразу) поймешь проблему.'''
            },
            'Futuro perfecto compuestas comunes': {
                '1: Действие будет завершено до другого момента в будущем<br>2: Гипотеза о прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Обещания и предсказания. Действие будет завершено до другого момента в будущем.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями "когда" о будущем времени.<br>
                    <b style="color: #7891BF">Пример: </b>Cuando lleguemos <u>habrán cerrado</u> las puertas.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Когда мы доберёмся, двери будут закрыты (сейчас они ещё открыты).<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Гипотеза или задаваться вопросом, интересоваться о прошлом. "Haber" указывает, что гипотеза касается прошлого.<br>
                    <b style="color: #7891BF">Пример: </b>Habrá anotado mal el número.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    (Я не знаю причину, но, вероятно,) он неправильно записал номер.'''
            },
            'Futuro perfecto con Ir a': {
                '1: Действие будет завершено до другого момента в будущем<br>2: Недоверие о прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Обещания и предсказания. Действие будет завершено до другого момента в будущем (неформальное).<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями "когда" о будущем.<br>
                    <b style="color: #7891BF">Пример: </b>Cuando vengas <u>voy a haber preparado</u> todo.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Когда ты придёшь (сюда), я (уже) всё приготовлю (но я ещё не приготовил).<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Удивление, недоверие, неодобрение или замешательство о прошлом.<br>
                    <b style="color: #7891BF">Пример: </b>Qué van a haber estado en la luna!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Они, должно быть, были на Луне!'''
            },
            'Presente subjuntivo': {
                'Сослагательное наклонение 1':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Придаточное предложение после "чтобы" или "что". Пожелания или требования.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в настоящем или будущем времени.<br>
                    <b style="color: #7891BF">Пример: </b>Ella quiere que la <u>ayudemos</u>.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Она хочет, чтобы мы ей помогли.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Espero que <u>puedas</u>.
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Надеюсь, что ты сможешь.<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    "Когда" (о будущем).<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в будущем времени или в повелительном наклонении.<br>
                    <b style="color: #7891BF">Пример: </b>Te escribiré cuando <u>llegue</u> a la oficina.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я напишу тебе, когда приеду в офис.<br><br>
                    <b style="color: #7891BF">Использование 3: </b> 
                    "Возможно" (о настоящем времени или о будущем).<br>
                    <b style="color: #7891BF">Пример: </b>Quizás lo <u>intentemos</u> de nuevo.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Возможно, мы попытаемся снова.'''
            },
            'Imperfecto subjuntivo': {
                'Сослагательное наклонение 2':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Придаточное предложение после "чтобы" или "что". Пожелания или требования.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени.<br>
                    <b style="color: #7891BF">Пример: </b>Ella nos pidió que la <u>ayudásemos</u>.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Она попросила нас, чтобы мы ей помогли.<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Невероятное или невозможное условие, в настоящем времени и в будущем ("если бы").<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями о последствиях, если условие выполнялось ("бы").<br>
                    <b style="color: #7891BF">Пример: </b>Si <u>tuviese</u> una lancha iría a la isla.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если бы у меня была лодка, я бы отправился на остров.'''
            },
            'Futuro subjuntivo': {
                'Сослагательное наклонение 3':
                '''<b style="color: #7891BF">Использование: </b>
                    Вероятное и возможное условие, в будущем ("если" или "когда"). Очень официально. Обычно в юридических текстах.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в будущем.<br>
                    <b style="color: #7891BF">Пример: </b>Si el proveedor no <u>entregare</u> el producto dentro de los tres días habiles, la empresa podrá rescindir el contrato.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если поставщик не доставит товар в течение трёх рабочих дней, компания сможет расторгнуть договор.'''
            },
            'Pluscuamperfecto compuestos del subjuntivo': {
                'Сослагательное наклонение 2 в прошлом (так не произошло)':
                '''<b style="color: #7891BF">Использование: </b>
                    Условие, которое не исполнилось в прошлом и уже невозможно ("если бы"). "Haber" отодвигает условие в прошлое.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями о последствиях, которые не были выполнены в прошлом ("бы").<br>
                    <b style="color: #7891BF">Примеры: Si ella me <u>hubiese dicho</u> que iba a venir con amigos, habría preparado más comida.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если бы она сказала мне (но не сказала), что она собиралась прийти с друзьями, я бы приготовил больше еды (но не приготовил).<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Si mi abuela no <u>se hubiese muerto</u>, estaría viva. (выражение)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если бы моя бабушка не умерла (но она умерла), она была бы жива.'''
            },
            'Condicional indicativo': {
                '1: Условие "бы"<br>2: Предсказание в прошлом':
                '''<b style="color: #7891BF">Использование 1: </b>
                    Последствие если условие выполняется. Совет.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в сослагательном наклонении 2.<br>
                    <b style="color: #7891BF">Примеры: </b>Si tuviese mis herramientas aquí lo <u>repararía</u>.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если бы у меня были здесь инструменты, я бы его починил.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Yo no iría a ese lugar.
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я бы туда не пошёл.<br><br>
                    <b style="color: #7891BF">Использование 2: </b> 
                    Предсказание в прошлом.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в прошедшем времени.<br>
                    <b style="color: #7891BF">Пример: </b>Creí que <u>sería</u> más difícil.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Я думал, что <u>будет</u> сложнее.'''
            },
            'Condicional perfecto compuestas comunes': {
                'Условие "бы" в прошлом (так и не произошло)':
                '''<b style="color: #7891BF">Использование: </b>
                    Последствие, которое не было выполнено в прошлом и уже невозможно. "Haber" отодвигает последствие в прошлое.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    В сочетании с предложениями в сослагательном наклонении (уже невозможно).<br>
                    <b style="color: #7891BF">Пример: Si hubiésemos sabido cómo se comporta la gente aquí en año nuevo, <u>habríamos viajado</u> en otro momento.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Если бы мы знали (но не знали), как люди ведут себя здесь в Новый год, мы бы путешествовали в другой момент (но мы уже здесь).'''
            },
            'Podria haber': {
                'Условие "бы мог" в прошлом (так и не произошло)':
                '''<b style="color: #7891BF">Использование: </b>
                    Действие, которое не произошло, но было возможно в прошлом. "Haber" отодвигает возможность в прошлое.<br>
                    <b style="color: #7891BF">Пример: ¡Podrías haber incendiado la casa con tus experimentos!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Ты мог бы поджечь дом (но не поджёг и риск уже исчез) своими экспериментами!'''
            },
            'Deberia haber': {
                'Условие "бы следовало" (так и не произошло)':
                '''<b style="color: #7891BF">Использование: </b>
                    Желаемое действие, которое не произошло и уже поздно. "Haber" отодвигает возможность в прошлое.<br>
                    <b style="color: #7891BF">Пример: <u>Deberíamos haber comprado</u> oro hace dos años.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    Нам следовало купить золото (но мы не купили и уже поздно) два года назад.'''
            },
            'Puede haber': {
                'Гипотеза о прошлом':
                '''<b style="color: #7891BF">Использование: </b>
                    Гипотеза о прошлом (низкий уровень уверенности). "Haber" отодвигает возможность в прошлое.<br>
                    <b style="color: #7891BF">Пример: <u>Pueden haber cambiado</u> la clave y no nos han dicho nada.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    (Я не знаю причину, но одна из возможностей, что) они сменили пароль и (пока) не сообщили нам об этом.'''
            },
            'Debe haber': {
                'Вывод о прошлом':
                '''<b style="color: #7891BF">Использование: </b>
                    Вывод о прошлом (высокий уровень уверенности). "Haber" отодвигает вывод на действие прошлого.<br>
                    <b style="color: #7891BF">Пример: Debe haberse quedado dormido.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                     (Я почти уверен, что) он проспал.'''
            }
        }

        filtered_conjugations = {}

        for tense, pronouns in conjugations.items():
            rus_tense = esp_to_rus_dict.get(tense, tense)
            filtered_conjugations[rus_tense] = {}
            for pronoun, conjugation in pronouns.items():
                if pronoun.lower() not in accents:
                    filtered_conjugations[rus_tense][pronoun] = conjugation

        return filtered_conjugations
