import requests
from bs4 import BeautifulSoup

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