import csv
from create_dict_rows import create_dict_rows


def write_to_csv():
    """
    Function write to csv file all data as a table
    """
    dict_rows = create_dict_rows()
    hotel_info = ['hotel_name', 'location', 'price', 'score', 'reviews', 'url']

    with open('hotels.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=hotel_info)
        writer.writeheader()
        writer.writerows(dict_rows)

write_to_csv()