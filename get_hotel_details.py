import grequests
from get_soup import get_soup
import conf as CFG
from create_dict_rows import create_dict_rows
from bs4 import BeautifulSoup
from fake_headers import Headers
from random import random

def get_hotel_details():
    """
    !!!GREQUESTS. FUNCTION NOT USED RIGHT NOW
    Takes in a list of url and requests to them IN BATCH (grequests is used)
    :param url_list: List of url that you want to get response from
    :return: response
    """

    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

    hotels_dict = create_dict_rows()
    all_hotel_urls = [hotel['url'] for hotel in hotels_dict]
    print(all_hotel_urls[0:20])


    for i in range(0, len(all_hotel_urls), CFG.BATCH_SIZE):
        print(len(all_hotel_urls))
        urls_batch = all_hotel_urls[i:i + CFG.BATCH_SIZE]
        random_header = header.generate()
        response = (grequests.get(url, headers=random_header) for url in urls_batch)
        print(random_header)
        for rs in grequests.map(response):
            soup = BeautifulSoup(rs.text, "html.parser")
            try:
                name = soup.find(class_='pp-header__title').text
                print(f'{name}: {rs.url}')
            except AttributeError:
                print(f'NOT FOUND: {rs.url}')
                # # logger.info(f'{rs.url}\n{soup}')
                # with open("output1.html", "w", encoding='utf-8') as file:
                #     file.write(str(soup))
                # quit()

            # quit()







get_hotel_details()