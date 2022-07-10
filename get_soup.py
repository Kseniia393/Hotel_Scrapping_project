import conf as CFG
import requests
from bs4 import BeautifulSoup

def get_soup(url):
    headers = CFG.HEADERS
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup