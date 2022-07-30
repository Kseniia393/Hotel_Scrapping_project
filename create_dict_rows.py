import grequests
import requests
import conf as CFG
from get_urls import get_urls
from bs4 import BeautifulSoup
import re
import pymysql.cursors
from datetime import date


def create_dict_rows():
    """
    Creates a dictionary that represents by itself a row of a future table.
    As a key we use names of the columns.
    :return: list of dictionaries
    """
    url_list, city, check_in_date, check_out_date, adults = get_urls()
    response = (grequests.get(link, headers=CFG.HEADERS) for link in url_list)
    dict_rows = []
    for rs in grequests.map(response):
        soup = BeautifulSoup(rs.text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')

        for hotel in hotels:
            hotel_title = hotel.findChild('div', class_='fcab3ed991 a23c043802').text

            location = hotel.findChild('span', class_='f4bd0794db b4273d69aa').text
            if re.search(r'(,\s)', location):
                hotel_area, hotel_city = location.split(', ')
            else:
                hotel_area, hotel_city = None, location

            price = hotel.findChild('span', class_='fcab3ed991 bd73d13072')
            if price is not None:
                price = price.text
                price = int(re.findall(r'\d+', price)[0])
            else:
                price = None

            hotel_score = hotel.findChild('div', class_='b5cd09854e d10a6220b4')
            if hotel_score is not None:
                hotel_score = hotel_score.text
            else:
                hotel_score = None

            hotel_review = hotel.findChild('div', class_='d8eab2cf7f c90c0a70d3 db63693c62')
            if hotel_review is not None:
                hotel_review = int(re.findall(r'\d+', hotel_review.text.replace(',', ''))[0])
            else:
                hotel_review = None

            url = hotel.findChild('a').get('href')
# --------------------------------------------------------------
            rs_hotel = requests.get(url, headers=CFG.HEADERS)

            soup = BeautifulSoup(rs_hotel.text, "html.parser")
            facilities_scores = soup.find_all('span', class_='c-score-bar__title')
            score_dict = {}
            for fac_score in facilities_scores:
                score_dict[fac_score.text.rstrip("\xa0")] = fac_score.find_next_sibling("span").text

            if 'Location' in score_dict:
                hotel_loc_score = float(score_dict['Location'])
            else:
                hotel_loc_score = None

# --------------------------------------------------------------
# WORK WITH DB - TABLE - hotels
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='DEFAULT_PASSWORD',
                                         database='hotels_booking',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            sql_select_id = f'SELECT id_hotel FROM hotels WHERE hotel_title LIKE "{hotel_title}" AND hotel_city LIKE "{hotel_city}"'
            cursor.execute(sql_select_id)
            id_hotel = cursor.fetchall()
            if len(id_hotel) != 0:
                id_hotel = id_hotel[0]['id_hotel']
                sql_update = """UPDATE hotels SET hotel_score=%s, hotel_review=%s, hotel_loc_score=%s
                                    WHERE id_hotel=%s"""
                cursor.execute(sql_update, (hotel_score, hotel_review, hotel_loc_score, id_hotel))
                connection.commit()

            else:
                sql_insert = """INSERT INTO hotels 
                (hotel_title, hotel_score, hotel_review, hotel_loc_score, hotel_area, hotel_city)
                VALUES (%s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql_insert, (hotel_title, hotel_score, hotel_review, hotel_loc_score, hotel_area, hotel_city))
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
            if 'Staff' in score_dict:
                staff_score = float(score_dict['Staff'])
            else:
                staff_score = None

            if 'Free WiFi' in score_dict:
                wifi_score = float(score_dict['Free WiFi'])
            else:
                wifi_score = None

            if 'Cleanliness' in score_dict:
                clean_score = float(score_dict['Cleanliness'])
            else:
                clean_score = None

# --------------------------------------------------------------
# WORK WITH DB - TABLE - facilities AND hotels_facilities

            facilities = soup.find('div', class_='hotel-facilities__list')
            facilities_list = [facility.text.split('\n') for facility in facilities]
            facilities_list = sum(facilities_list, [])
            if 'Non-smoking rooms' in facilities_list:
                non_smoking = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE 'Non-smoking rooms'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                non_smoking = False

            if 'Business centre' in facilities_list:
                business_center = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE 'Business centre'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                business_center = False

            if 'Free parking' in facilities_list:
                free_parking = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE 'Free parking'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                free_parking = False

            if '24-hour front desk' in facilities_list:
                front_desk_24_7 = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE '24-hour front desk'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                front_desk_24_7 = False

            if 'Laundry' in facilities_list:
                laundry = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE 'Laundry'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                laundry = False

            if 'Airport shuttle' in facilities_list:
                shuttle = True
                sql_select_id = """SELECT id_facilities FROM facilities WHERE facilities_title LIKE 'Airport shuttle'"""
                cursor.execute(sql_select_id)
                id_facilities = cursor.fetchall()[0]['id_facilities']

                cursor.execute("""SELECT id FROM hotels_facilities WHERE id_hotel=%s AND id_facilities=%s""", (id_hotel, id_facilities))
                if len(cursor.fetchall()) == 0:
                    sql_insert = """INSERT INTO hotels_facilities (id_hotel, id_facilities) VALUES (%s, %s)"""
                    cursor.execute(sql_insert, (id_hotel, id_facilities))
                    connection.commit()
                else:
                    pass
            else:
                shuttle = False


# --------------------------------------------------------------
#             dict_rows.append({'hotel_name': hotel_title, 'area': area, 'city': city,
#                               'price': price, 'score': hotel_score, 'reviews': hotel_review,
#                               'hotel_loc_score': hotel_loc_score, 'staff_score': staff_score,
#                               'wifi_score': wifi_score, 'clean_score': clean_score,
#                               'non_smoking': non_smoking, 'business_center': business_center,
#                               'free_parking': free_parking, 'front_desk_24_7': front_desk_24_7,
#                               'laundry': laundry, 'shuttle': shuttle})

    return dict_rows
