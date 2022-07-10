import csv
from create_dict_rows import create_dict_rows


def write_to_csv():
    dict_rows = create_dict_rows()
    hotel_info = ['hotel_name', 'location', 'price', 'score', 'reviews']

    with open('hotels.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=hotel_info)
        writer.writeheader()
        writer.writerows(dict_rows)

write_to_csv()