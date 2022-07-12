import re
from get_soup import get_soup


def get_total_hotel_nums(url_search) -> int:
    """
    Function parse on the url amd find number of all hotels according to transmitted request date.
    Use this value to create offset number.
    :param url_search:
    :return: integer number of all hotels
    """
    soup = get_soup(url_search)
    total_hotels = soup.find("div", class_="efdb2b543b").text
    total_hotels = int(re.findall(r'\d+', total_hotels)[0])
    return total_hotels
