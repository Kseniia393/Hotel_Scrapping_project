import grequests
import conf as CFG
from get_urls import get_urls
from bs4 import BeautifulSoup
import re


def create_dict_rows():
    """
    Creates a dictionary that represents by itself a row of a future table.
    As a key we use names of the columns.
    :return: list of dictionaries
    """
    url_list = get_urls()
    response = (grequests.get(link, headers=CFG.HEADERS) for link in url_list)
    dict_rows = []
    for rs in grequests.map(response):
        soup = BeautifulSoup(rs.text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')

        for hotel in hotels:
            name = hotel.findChild('div', class_='fcab3ed991 a23c043802').text
            location = hotel.findChild('span', class_='f4bd0794db b4273d69aa').text

            price = hotel.findChild('span', class_='fcab3ed991 bd73d13072').text
            price = int(re.findall(r'\d+', price)[0])

            score = hotel.findChild('div', class_='b5cd09854e d10a6220b4')

            if score is not None:
                score = score.text
            else:
                score = None

            reviews = hotel.findChild('div', class_='d8eab2cf7f c90c0a70d3 db63693c62')
            if reviews is not None:
                reviews = reviews.text
            else:
                reviews = None

            url = hotel.findChild('a').get('href')

            dict_rows.append({'hotel_name': name, 'location': location,
                              'price': price, 'score': score, 'reviews': reviews, 'url': url})



    return dict_rows
