import requests
import conf as CFG
from get_urls import get_urls
from bs4 import BeautifulSoup
import re
import pymysql.cursors
from datetime import date
from create_DB import create_db, create_db_tables
from tqdm.auto import tqdm


def scrape_hotel(hotel_soup):
    """
    Scrap part of soup to get hotel data from the main page
    :param hotel_soup:
    :return: hotel_title, hotel_area, hotel_city, price, hotel_score, hotel_review, url
    """
    hotel_title = hotel_soup.findChild('div', class_='fcab3ed991 a23c043802').text

    location = hotel_soup.findChild('span', class_='f4bd0794db b4273d69aa').text
    if re.search(r'(,\s)', location):
        hotel_area, hotel_city = location.split(', ')
    else:
        hotel_area, hotel_city = None, location

    price = hotel_soup.findChild('span', class_='fcab3ed991 bd73d13072')
    if price is not None:
        price = price.text
        price = int(re.findall(r'\d+', price)[0])
    else:
        price = None

    hotel_score = hotel_soup.findChild('div', class_='b5cd09854e d10a6220b4')
    if hotel_score is not None:
        hotel_score = hotel_score.text
    else:
        hotel_score = None

    hotel_review = hotel_soup.findChild('div', class_='d8eab2cf7f c90c0a70d3 db63693c62')
    if hotel_review is not None:
        hotel_review = int(re.findall(r'\d+', hotel_review.text.replace(',', ''))[0])
    else:
        hotel_review = None

    url = hotel_soup.findChild('a').get('href')
    return hotel_title, hotel_area, hotel_city, price, hotel_score, hotel_review, url


def scrap_scores(score_dict):
    """
    Scrap hotel page and get different scores: Location, Staff, Free WiFi, Cleanliness,
    if they are presented on the page
    :param score_dict:
    :return:
    """
    if 'Location' in score_dict:
        hotel_loc_score = float(score_dict['Location'])
    else:
        hotel_loc_score = None

    if 'Staff' in score_dict:
        hotel_staff_score = float(score_dict['Staff'])
    else:
        hotel_staff_score = None

    if 'Free WiFi' in score_dict:
        hotel_wifi_score = float(score_dict['Free WiFi'])
    else:
        hotel_wifi_score = None

    if 'Cleanliness' in score_dict:
        hotel_cleanliness_score = float(score_dict['Cleanliness'])
    else:
        hotel_cleanliness_score = None
    return hotel_loc_score, hotel_staff_score, hotel_wifi_score, hotel_cleanliness_score


def scrap_facilities(soup):
    """
    Scrap hotel page and get different facilities
    :param soup:
    :return: facilities_list
    """
    facilities = soup.find('div', class_='hotel-facilities__list')
    facilities_list = [facility.text.split('\n') for facility in facilities]
    facilities_list = sum(facilities_list, [])
    return facilities_list


def write_facilities_to_DB(facility, facilities_list, cursor, connection, id_hotel):
    """
    Write to DB facility of the hotel
    :param facility:
    :param facilities_list:
    :return: None
    """
    if facility in facilities_list:
        sql_select_id = f"""SELECT id_facilities FROM facilities WHERE facilities_title LIKE '{facility}'"""
        cursor.execute(sql_select_id)
        id_facilities = cursor.fetchall()[0]['id_facilities']

        cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""",
                       (id_hotel, id_facilities))
        if len(cursor.fetchall()) == 0:
            sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
            cursor.execute(sql_insert, (id_hotel, id_facilities))
            connection.commit()
        else:
            pass
    else:
        pass


def write_to_db(city, check_in_date, check_out_date, adults, PASSWORD):
    """
    Parse from the website and write to DB
    """
    create_db(PASSWORD)
    create_db_tables(PASSWORD)

    url_list = get_urls(city, check_in_date, check_out_date, adults)
    response = [requests.get(url, headers=CFG.HEADERS) for url in url_list]

    for i in tqdm(range(len(response))):
        soup = BeautifulSoup(response[i].text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')

        for hotel in hotels:

            hotel_title, hotel_area, hotel_city, price, hotel_score, hotel_review, url = scrape_hotel(hotel)

            rs_hotel = requests.get(url, headers=CFG.HEADERS)
            soup = BeautifulSoup(rs_hotel.text, "html.parser")
            facilities_scores = soup.find_all('span', class_='c-score-bar__title')
            score_dict = {}
            for fac_score in facilities_scores:
                score_dict[fac_score.text.rstrip("\xa0")] = fac_score.find_next_sibling("span").text

            hotel_loc_score, hotel_staff_score, hotel_wifi_score, hotel_cleanliness_score = scrap_scores(score_dict)

            # --------------------------------------------------------------
            # WORK WITH DB - TABLE - hotels
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password=PASSWORD,
                                         database='hotels_booking',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            sql_select_id = f'SELECT id_hotel FROM hotels WHERE hotel_title LIKE "{hotel_title}" AND hotel_city LIKE "{hotel_city}"'
            cursor.execute(sql_select_id)
            id_hotel = cursor.fetchall()
            if len(id_hotel) != 0:
                id_hotel = id_hotel[0]['id_hotel']
                sql_update = """UPDATE hotels SET hotel_score=%s, hotel_review=%s, hotel_loc_score=%s,
                hotel_staff_score=%s, hotel_wifi_score=%s, hotel_cleanliness_score=%s
                                    WHERE id_hotel=%s"""
                cursor.execute(sql_update, (hotel_score, hotel_review, hotel_loc_score, hotel_staff_score, hotel_wifi_score, hotel_cleanliness_score, id_hotel))
                connection.commit()

            else:
                sql_insert = """INSERT INTO hotels 
                (hotel_title, hotel_score, hotel_review, hotel_loc_score, hotel_staff_score, 
                hotel_wifi_score, hotel_cleanliness_score, hotel_area, hotel_city)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql_insert,
                               (hotel_title, hotel_score, hotel_review, hotel_loc_score, hotel_staff_score, hotel_wifi_score, hotel_cleanliness_score, hotel_area, hotel_city))
                connection.commit()
                sql_select_id = f'SELECT id_hotel FROM hotels WHERE hotel_title LIKE "{hotel_title}" AND hotel_city LIKE "{hotel_city}"'
                cursor.execute(sql_select_id)
                id_hotel = cursor.fetchall()[0]['id_hotel']
            # --------------------------------------------------------------
            # WORK WITH DB - TABLE - search_params
            sql_select_id = f"""SELECT id_search FROM search_params 
                                WHERE city LIKE '{city}' AND check_in_date LIKE '{check_in_date}'
                                AND check_out_date LIKE '{check_out_date}'
                                AND adults LIKE '{adults}'"""
            cursor.execute(sql_select_id)
            id_search = cursor.fetchall()
            if len(id_search) == 0:
                sql_insert = """INSERT INTO search_params (city, check_in_date, check_out_date, adults)
                VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql_insert, (city, check_in_date, check_out_date, adults))
                connection.commit()

                sql_select_id = f"""SELECT id_search FROM search_params 
                                                WHERE city LIKE '{city}' AND check_in_date LIKE '{check_in_date}'
                                                AND check_out_date LIKE '{check_out_date}'
                                                AND adults LIKE '{adults}'"""
                cursor.execute(sql_select_id)
                id_search = cursor.fetchall()[0]['id_search']
            else:
                id_search = id_search[0]['id_search']
            # --------------------------------------------------------------
            # WORK WITH DB - TABLE - price
            sql_insert = """INSERT INTO price (id_hotel, id_search, timestamp, cheapest_price)
                            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql_insert, (id_hotel, id_search, date.today(), price))
            connection.commit()

            # --------------------------------------------------------------
            # WORK WITH DB - TABLE - facilities AND hotels_facilities

            facilities_list = scrap_facilities(soup)

            for facility in CFG.FACILITIES:
                write_facilities_to_DB(facility, facilities_list, cursor, connection, id_hotel)
