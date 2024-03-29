from typing import Tuple, List, Any
import re
from bs4 import BeautifulSoup
import requests
import conf as CFG


def get_total_hotel_nums(url) -> int:
    """
    Function parses the url and finds number of all hotels according to transmitted request date.
    Uses this value to create offset number.
    :param url: url of the first search page
    :return: integer number of all hotels
    """
    response = requests.get(url, headers=CFG.HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    total_hotels = soup.find("div", class_="efdb2b543b").text
    total_hotels = int(re.findall(r'\d+', total_hotels)[0])
    return total_hotels


def create_url(hotel_dict, off_set=0):
    """
    Function creates the initial url for hotel search.
    Arguments city (-c), check in date (-i), check out date (-o), number of people (-p) are parsed from the CLI.
    Default arguments: telaviv 2022-12-31 2023-01-01 2
    :param off_set: number of searching page (be contained without remainder on 25)
    :return: url with first page of searching
    """

    url = "https://www.booking.com/searchresults.html?" \
          "checkin={check_in}" \
          "&checkout={check_out}" \
          "&group_adults={group_adults}" \
          "&group_children=0&order=score" \
          "&ss={city}" \
          "&selected_currency=USD" \
          "&offset={limit}".format(
        check_in=hotel_dict['check_in_date'],
        check_out=hotel_dict['check_out_date'],
        group_adults=hotel_dict['adults'],
        limit=off_set,
        city=hotel_dict['city'])
    return url


def get_urls(hotel_dict) -> tuple[list[Any], Any, Any, Any, Any]:
    """
    Generates all pages of the  search
    :return: list of urls of all pages in the search
    """
    url = create_url(hotel_dict)
    total_hotel_nums = get_total_hotel_nums(url)
    url_list = [url]
    url_range = (total_hotel_nums//CFG.HOTELS_PER_PAGE)*CFG.HOTELS_PER_PAGE
    url_base = url[:-1]
    for i in range(0, url_range, CFG.HOTELS_PER_PAGE):
        url_next = url_base + str(i + CFG.HOTELS_PER_PAGE)
        url_list.append(url_next)
    return url_list




