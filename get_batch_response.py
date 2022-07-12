import grequests
from get_soup import get_soup
import conf as CFG



def get_batch_response(url_list):
    """
    NB! Currently not used but saved for future purposes.
    Takes in a list of url and requests to them IN BATCH (grequests is used)
    :param url_list: List of url that you want to get response from
    :return: response
    """
    response = (grequests.get(url, headers = CFG.HEADERS) for url in url_list)
    response = grequests.map(response)
    return response