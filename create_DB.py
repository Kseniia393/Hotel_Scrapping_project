import pymysql.cursors


def create_db(PASSWORD):
    """Crete DB if not exist yet"""
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=PASSWORD,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE DATABASE hotels_booking""")
    except:  # TODO - specific exception to be raised
        pass


def create_db_tables(PASSWORD):
    """Create Tables in DB and Insert values into table facilities"""
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=PASSWORD,
                                 database='hotels_booking',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE hotels (
                          id_hotel INT PRIMARY KEY AUTO_INCREMENT,
                          hotel_title VARCHAR(150),
                          hotel_score FLOAT,
                          hotel_review INT,
                          hotel_loc_score FLOAT,
                          hotel_area VARCHAR(50),
                          hotel_city VARCHAR(50))""")

        cursor.execute("""CREATE TABLE facilities (
                          id_facilities INT PRIMARY KEY AUTO_INCREMENT,
                          facilities_title VARCHAR(50))""")

        cursor.execute("""CREATE TABLE hotels_facilities (
                          id INT PRIMARY KEY AUTO_INCREMENT,
                          id_hotel INT,
                          id_facilities INT,
                          FOREIGN KEY (id_hotel) REFERENCES hotels(id_hotel),
                          FOREIGN KEY (id_facilities) REFERENCES facilities(id_facilities))""")

        cursor.execute("""CREATE TABLE search_params (
                          id_search INT PRIMARY KEY AUTO_INCREMENT,
                          city VARCHAR(25),
                          check_in_date DATE,
                          check_out_date DATE,
                          adults INT)""")

        cursor.execute("""CREATE TABLE price (
                          id_price INT PRIMARY KEY AUTO_INCREMENT,
                          id_hotel INT NOT NULL,
                          id_search INT NOT NULL,
                          timestamp DATE,
                          cheapest_price INT,
                          FOREIGN KEY (id_hotel) REFERENCES hotels(id_hotel),
                          FOREIGN KEY (id_search) REFERENCES search_params(id_search))""")

        cursor.executemany("""INSERT INTO facilities (facilities_title) VALUES (%s)""",
                           [('Non-smoking rooms'), ('Business centre'), ('Free parking'), ('24-hour front desk'),
                            ('Laundry'), ('Airport shuttle')])
        connection.commit()
    except:  # TODO - specific exception to be raised
        pass
