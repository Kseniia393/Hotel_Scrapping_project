# from write_to_db import write_to_db
import time
import argparse
import requests
import logging
import sys
import conf as CFG
from create_DB import create_db, create_db_tables
from get_urls import get_urls
from write_to_db import write_to_db
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from scrap_data import scrap_facilities, scrape_hotel, scrap_scores
from api import get_hotel_google_score


# book_scrap_log setting
logger = logging.getLogger('book_scrap_log')
logger.setLevel(logging.DEBUG)
# standard log output
stream_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%I:%M:%S')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)
# file log out
file_formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S')
file_handler = logging.FileHandler(CFG.LOG_FILE + '.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def parse_cli():
    """
    Parses arguments from CLI.
    :return: CLI arguments (city, check_in_date, check_out_date, adults, CFG.PASSWORD)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--city", default="Tel Aviv", help='Enter city name in any format. Default is "Tel Aviv"')
    parser.add_argument('-i', "--check_in_date", default="2022-12-31", help='Enter check in date in format yyyy-mm-dd. Default is "2022-12-31"')
    parser.add_argument('-o', "--check_out_date", default="2023-01-01", help='Enter check out date in format yyyy-mm-dd. Default is "2023-01-01"')
    parser.add_argument('-a', "--adults", default="2", help='Enter number of adults travelling (integer). Default is "2"')
    parser.add_argument('-p', "--password", help='Enter password to mysql db. It will not be saved in the code')
    parser.add_argument('-k', "--key", help='Enter Google Engine API key. It will not be saved in the code')

    args = parser.parse_args()

    city = args.city
    check_in_date = args.check_in_date
    check_out_date = args.check_out_date
    adults = args.adults
    CFG.PASSWORD = args.password
    CFG.API_KEY = args.key

    return city, check_in_date, check_out_date, adults, CFG.PASSWORD


def main():
    """
    Acts as an orchestrator to program functions.
    Calls different functions to get CLI apguments, generate urls, scrap data, write to the DB.
    :return: None
    """

    hotel_dict = {}
    hotel_dict['city'], hotel_dict['check_in_date'], hotel_dict['check_out_date'], hotel_dict[
        'adults'], CFG.PASSWORD = parse_cli()

    logger.info('Creating database with tables')
    # check if DB and tables are in place, if not, create them:
    create_db(CFG.PASSWORD)
    create_db_tables(CFG.PASSWORD)

    # generate all urls of the search result:
    url_list = get_urls(hotel_dict)

    logger.info('Creating list of responses for all hotels')
    # create list of responses for all search urls:
    response = [requests.get(url, headers=CFG.HEADERS) for url in url_list]

    logger.info('Parsing hotels...')
    # get hotel data from all search urls:
    for i in tqdm(range(len(response))):
        soup = BeautifulSoup(response[i].text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')
        for hotel in hotels:
            hotel_dict['hotel_title'], hotel_dict['hotel_area'], hotel_dict['hotel_city'], hotel_dict['price'], \
            hotel_dict['hotel_score'], hotel_dict['hotel_review'], hotel_dict['url'] = scrape_hotel(hotel)

            logger.debug(f"Parsing hotel: {hotel_dict['hotel_title']}")
            # print(hotel_dict['hotel_title'])

            rs_hotel = requests.get(hotel_dict['url'], headers=CFG.HEADERS)
            hotel_dict['soup'] = BeautifulSoup(rs_hotel.text, "html.parser")
            facilities_scores = hotel_dict['soup'].find_all('span', class_='c-score-bar__title')
            score_dict = {}

            for fac_score in facilities_scores:
                score_dict[fac_score.text.rstrip("\xa0")] = fac_score.find_next_sibling("span").text

            hotel_dict['hotel_loc_score'], hotel_dict['hotel_staff_score'], hotel_dict['hotel_wifi_score'], \
            hotel_dict['hotel_cleanliness_score'] = scrap_scores(score_dict)

            hotel_dict['facilities_list'] = scrap_facilities(hotel_dict['soup'])
            query_for_api = hotel_dict['hotel_title'] + hotel_dict['hotel_city']
            try:
                hotel_dict['hotel_google_score'] = get_hotel_google_score(query_for_api)
            except KeyError:
                logger.debug("doesn't recieved hotel_google_score")
                hotel_dict['hotel_google_score'] = None

            # write all collected data to the DB:
            write_to_db(CFG.PASSWORD, hotel_dict)
    logger.info('TADAAAAAM')


start_time = time.time()
if __name__ == '__main__':
    main()
print("--- %s seconds ---" % (time.time() - start_time))
