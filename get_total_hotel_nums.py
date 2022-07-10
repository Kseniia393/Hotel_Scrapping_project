import conf as CFG
import requests
from bs4 import BeautifulSoup
import re

def get_total_hotel_nums(url_search) ->int:
    headers = CFG.HEADERS
    response = requests.get(url_search, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    total_hotels = soup.find("div", class_="efdb2b543b").text
    total_hotels = int(re.findall(r'\d+', total_hotels)[0])
    return total_hotels