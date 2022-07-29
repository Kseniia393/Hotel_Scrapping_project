import pymysql.cursors

connection = pymysql.connect(host='localhost',
                       user='root',
                       password='DEFAULT_PASSWORD',
                       cursorclass=pymysql.cursors.DictCursor)


def make_sql_query(sql):
    """
    Execute sql query
    :param sql: sql query
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    return


make_sql_query("""CREATE DATABASE hotels_booking""")

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='DEFAULT_PASSWORD',
                             database='hotels_booking',
                             cursorclass=pymysql.cursors.DictCursor)

make_sql_query("""CREATE TABLE hotels (
                  id_hotel INT PRIMARY KEY AUTO_INCREMENT,
                  hotel_title VARCHAR(150),
                  hotel_score FLOAT,
                  hotel_review INT,
                  hotel_loc_score FLOAT,
                  hotel_area VARCHAR(50),
                  hotel_city VARCHAR(50))""")

make_sql_query("""CREATE TABLE facilities (
                  id_facilities INT PRIMARY KEY AUTO_INCREMENT,
                  facilities_title VARCHAR(50))""")

make_sql_query("""CREATE TABLE hotels_facilities (
                  id INT PRIMARY KEY AUTO_INCREMENT,
                  id_hotel INT,
                  id_facilities INT,
                  FOREIGN KEY (id_hotel) REFERENCES hotels(id_hotel),
                  FOREIGN KEY (id_facilities) REFERENCES facilities(id_facilities))""")

make_sql_query("""CREATE TABLE search_params (
                  id_search INT PRIMARY KEY AUTO_INCREMENT,
                  city VARCHAR(25),
                  check_in_date DATE,
                  check_out_date DATE,
                  adults INT)""")

make_sql_query("""CREATE TABLE price (
                  id_price INT PRIMARY KEY AUTO_INCREMENT,
                  id_hotel INT NOT NULL,
                  id_search INT NOT NULL,
                  timestamp DATE,
                  cheapest_price INT,
                  FOREIGN KEY (id_hotel) REFERENCES hotels(id_hotel),
                  FOREIGN KEY (id_search) REFERENCES search_params(id_search))""")