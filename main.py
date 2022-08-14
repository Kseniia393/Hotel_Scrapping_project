# from write_to_db import write_to_db
import time
import argparse
import conf as CFG
from create_DB import create_db, create_db_tables
from get_urls import get_urls
from write_to_db import write_to_db
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from scrap_data import scrap_facilities, scrape_hotel, scrap_scores


def parse_cli():
    """
    Parses arguments from CLI.
    :return: CLI arguments (city, check_in_date, check_out_date, adults, CFG.PASSWORD)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--city", default="Tel Aviv")
    parser.add_argument('-i', "--check_in_date", default="2022-12-31")
    parser.add_argument('-o', "--check_out_date", default="2023-01-01")
    parser.add_argument('-a', "--adults", default="2")
    parser.add_argument('-p', "--password")
    args = parser.parse_args()

    city = args.city
    check_in_date = args.check_in_date
    check_out_date = args.check_out_date
    adults = args.adults
    CFG.PASSWORD = args.password

    return city, check_in_date, check_out_date, adults, CFG.PASSWORD


def main():
    '''
    Acts as an orchestrator to program functions.
    Calls different functions to get CLI apguments, generate urls, scrap data, write to the DB.
    :return: None
    '''

    hotel_dict = {}
    hotel_dict['city'], hotel_dict['check_in_date'], hotel_dict['check_out_date'], hotel_dict[
        'adults'], CFG.PASSWORD = parse_cli()

    # check if DB and tables are in place, if not, create them:
    create_db(CFG.PASSWORD)
    create_db_tables(CFG.PASSWORD)

    # generate all urls of the search result:
    url_list = get_urls(hotel_dict)

    # create list of responses for all search urls:
    response = [requests.get(url, headers=CFG.HEADERS) for url in url_list]

    # get hotel data from all search urls:
    for i in tqdm(range(len(response))):
        soup = BeautifulSoup(response[i].text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')
        for hotel in hotels:
            hotel_dict['hotel_title'], hotel_dict['hotel_area'], hotel_dict['hotel_city'], hotel_dict['price'], \
            hotel_dict['hotel_score'], hotel_dict['hotel_review'], hotel_dict['url'] = scrape_hotel(hotel)

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

            # write all collected data to the DB:
            write_to_db(CFG.PASSWORD, hotel_dict)


start_time = time.time()
if __name__ == '__main__':
    main()
print("--- %s seconds ---" % (time.time() - start_time))
