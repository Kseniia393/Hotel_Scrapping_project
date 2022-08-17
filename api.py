import requests


def get_hotel_google_score(query):
    """
    Uses Google search engine API to get information on number of searches done in google for each hotel.
    :param query: API query
    :return: number of searches done in google for each hotel (integer)
    """
    key = "AIzaSyBLqeARFRp_PUA6xaagPuowDkrPHNzwAtI"
    cx="719545adf2b7d4a0b"

    url = "https://www.googleapis.com/customsearch/v1?"

    querystring = {"key": key,
                   "cx": cx,
                   "q": query}

    response = requests.request("GET", url, params=querystring)
    response_json = response.json()
    hotel_google_score = response_json['queries']['request'][0]['totalResults']
    return int(hotel_google_score)

