import conf as CFG
from get_total_hotel_nums import get_total_hotel_nums
from create_url import create_url


def get_urls() -> list:
    url = create_url()
    total_hotel_nums = get_total_hotel_nums(url)
    url_list = [url]
    url_range = (total_hotel_nums//CFG.HOTELS_PER_PAGE)*CFG.HOTELS_PER_PAGE
    for i in range(0, url_range, CFG.HOTELS_PER_PAGE):
        url_next = create_url(off_set=i+CFG.HOTELS_PER_PAGE)
        url_list.append(url_next)
    return url_list




