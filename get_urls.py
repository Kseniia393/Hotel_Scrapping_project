import conf as CFG
from get_total_hotel_nums import get_total_hotel_nums


def get_urls(url_search) ->list:
    total_hotel_nums = get_total_hotel_nums(url_search)
    url_list = [url_search]
    url_base = url_search[:-1]
    url_range = (total_hotel_nums//CFG.HOTELS_PER_PAGE)*CFG.HOTELS_PER_PAGE
    for i in range(0, url_range, CFG.HOTELS_PER_PAGE):
        url_next = url_base + f'{i+CFG.HOTELS_PER_PAGE}'
        url_list.append(url_next)
    return url_list




