import csv
from create_dict_rows import create_dict_rows
import re

def write_to_csv():
    """
    Function writes to csv file all gathered data as a table
    """
    dict_rows = create_dict_rows()
    hotel_info = ['hotel_name', 'area', 'city', 'price', 'score', 'reviews', 'url']

    with open('hotels.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=hotel_info)
        writer.writeheader()
        writer.writerows(dict_rows)


def main():
    write_to_csv()


if __name__ == '__main__':
    main()