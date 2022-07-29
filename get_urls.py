from typing import Tuple, List, Any

import conf as CFG
from get_total_hotel_nums import get_total_hotel_nums
from create_url import create_url


def get_urls() -> tuple[list[Any], Any, Any, Any, Any]:
    """
    Function generate all pages of the same search
    :return: list of urls of all pages in the search
    """
    url, city, check_in_date, check_out_date, adults = create_url()
    total_hotel_nums = get_total_hotel_nums(url)
    url_list = [url]
    url_range = (total_hotel_nums//CFG.HOTELS_PER_PAGE)*CFG.HOTELS_PER_PAGE
    url_base = url[:-1]
    for i in range(0, url_range, CFG.HOTELS_PER_PAGE):
        url_next = url_base + str(i + CFG.HOTELS_PER_PAGE)
        url_list.append(url_next)
    return url_list, city, check_in_date, check_out_date, adults




