from bs4 import BeautifulSoup
import conf as CFG
import pymysql.cursors
from datetime import date
from scrap_data import scrap_scores, scrape_hotel


def write_facilities_to_DB(facility, facilities_list, cursor, connection, id_hotel):
    """
    Writes hotel facilities to the DB
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


def write_to_db(PASSWORD, hotel_dict):
    """
    Parse from the website and write to DB
    """
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=PASSWORD,
                                 database='hotels_booking',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()


    # --------------------------------------------------------------
    # TABLE - hotels

    sql_select_id = f'''SELECT id_hotel FROM hotels WHERE hotel_title LIKE "{hotel_dict['hotel_title']}" AND hotel_city LIKE "{hotel_dict['hotel_city']}"'''
    cursor.execute(sql_select_id)
    id_hotel = cursor.fetchall()
    if len(id_hotel) != 0:
        id_hotel = id_hotel[0]['id_hotel']
        sql_update = """UPDATE hotels SET hotel_score=%s, hotel_review=%s, hotel_loc_score=%s,
        hotel_staff_score=%s, hotel_wifi_score=%s, hotel_cleanliness_score=%s
                            WHERE id_hotel=%s"""
        cursor.execute(sql_update, (
        hotel_dict['hotel_score'], hotel_dict['hotel_review'], hotel_dict['hotel_loc_score'],
        hotel_dict['hotel_staff_score'], hotel_dict['hotel_wifi_score'],
        hotel_dict['hotel_cleanliness_score'], id_hotel))
        connection.commit()

    else:
        sql_insert = """INSERT INTO hotels 
        (hotel_title, hotel_score, hotel_review, hotel_loc_score, hotel_staff_score, 
        hotel_wifi_score, hotel_cleanliness_score, hotel_area, hotel_city)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(sql_insert,
                       (hotel_dict['hotel_title'], hotel_dict['hotel_score'], hotel_dict['hotel_review'],
                        hotel_dict['hotel_loc_score'], hotel_dict['hotel_staff_score'],
                        hotel_dict['hotel_wifi_score'], hotel_dict['hotel_cleanliness_score'], hotel_dict['hotel_area'],
                        hotel_dict['hotel_city']))
        connection.commit()
        sql_select_id = f'''SELECT id_hotel FROM hotels WHERE hotel_title LIKE "{hotel_dict['hotel_title']}" AND hotel_city LIKE "{hotel_dict['hotel_city']}"'''
        cursor.execute(sql_select_id)
        id_hotel = cursor.fetchall()[0]['id_hotel']
    # --------------------------------------------------------------
    # TABLE - search_params
    sql_select_id = f'''SELECT id_search FROM search_params 
                        WHERE city LIKE "{hotel_dict['city']}" AND check_in_date LIKE "{hotel_dict['check_in_date']}"
                        AND check_out_date LIKE "{hotel_dict['check_out_date']}"
                        AND adults LIKE "{hotel_dict['adults']}"'''
    cursor.execute(sql_select_id)
    id_search = cursor.fetchall()
    if len(id_search) == 0:
        sql_insert = """INSERT INTO search_params (city, check_in_date, check_out_date, adults)
        VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql_insert, (hotel_dict['city'], hotel_dict['check_in_date'], hotel_dict['check_out_date'],
                                    hotel_dict['adults']))
        connection.commit()


        cursor.execute(sql_select_id)
        id_search = cursor.fetchall()[0]['id_search']
    else:
        id_search = id_search[0]['id_search']
    # --------------------------------------------------------------
    #TABLE - price
    sql_insert = """INSERT INTO price (id_hotel, id_search, timestamp, cheapest_price)
                    VALUES (%s, %s, %s, %s)"""
    cursor.execute(sql_insert, (id_hotel, id_search, date.today(), hotel_dict['price']))
    connection.commit()

    # --------------------------------------------------------------
    # TABLE facilities AND hotels_facilities

    # facilities_list = scrap_facilities(hotel_dict['soup'])

    for facility in CFG.FACILITIES:
        write_facilities_to_DB(facility, hotel_dict['facilities_list'], cursor, connection, id_hotel)
