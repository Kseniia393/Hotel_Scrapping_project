import csv
from create_dict_rows import create_dict_rows
import re
import time
#fake-useragent

def write_to_csv():
    """
    Function writes to csv file all gathered data as a table
    """
    dict_rows = create_dict_rows()
    hotel_info = ['hotel_name', 'area', 'city', 'price', 'score', 'reviews', 'hotel_loc_score', 'staff_score',
                  'wifi_score', 'clean_score', 'non_smoking', 'business_center', 'free_parking', 'front_desk_24_7',
                  'laundry', 'shuttle']

    # dict_rows.append({'hotel_name': name, 'area': area, 'city': city,
    #                   'price': price, 'score': score, 'reviews': reviews,
    #                   'hotel_loc_score': hotel_loc_score, 'staff_score': staff_score,
    #                   'wifi_score': wifi_score, 'clean_score': clean_score,
    #                   'non_smoking': non_smoking, 'business_center': business_center,
    #                   'free_parking': free_parking, 'front_desk_24_7': front_desk_24_7,
    #                   'laundry': laundry, 'shuttle': shuttle
    #                   })

    with open('hotels.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=hotel_info)
        writer.writeheader()
        writer.writerows(dict_rows)


def main():
    write_to_csv()

start_time = time.time()
if __name__ == '__main__':
    main()
print("--- %s seconds ---" % (time.time() - start_time))