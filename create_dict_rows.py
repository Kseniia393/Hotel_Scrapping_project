import grequests
import requests
import conf as CFG
from get_urls import get_urls
from bs4 import BeautifulSoup
import re


def create_dict_rows():
    """
    Creates a dictionary that represents by itself a row of a future table.
    As a key we use names of the columns.
    :return: list of dictionaries
    """
    url_list = get_urls()
    response = (grequests.get(link, headers=CFG.HEADERS) for link in url_list)
    dict_rows = []
    for rs in grequests.map(response):
        soup = BeautifulSoup(rs.text, "html.parser")
        hotels = soup.find_all("div",
                               class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')

        for hotel in hotels:
            name = hotel.findChild('div', class_='fcab3ed991 a23c043802').text
            print(name)

            location = hotel.findChild('span', class_='f4bd0794db b4273d69aa').text
            if re.search(r'(\,\s)', location):
                area, city = location.split(', ')
            else:
                area, city = None, location

            price = hotel.findChild('span', class_='fcab3ed991 bd73d13072').text
            price = int(re.findall(r'\d+', price)[0])

            score = hotel.findChild('div', class_='b5cd09854e d10a6220b4')

            if score is not None:
                score = score.text
            else:
                score = None

            reviews = hotel.findChild('div', class_='d8eab2cf7f c90c0a70d3 db63693c62')
            if reviews is not None:
                reviews = int(re.findall(r'\d+', reviews.text.replace(',', ''))[0])
            else:
                reviews = None
            print(f'reviews: {reviews}')

            url = hotel.findChild('a').get('href')

#--------------------------------------------------------------
            rs_hotel_scores = requests.get(url, headers=CFG.HEADERS)

            soup = BeautifulSoup(rs_hotel_scores.text, "html.parser")
            facilities_scores = soup.find_all('span', class_='c-score-bar__title')
            score_dict={}
            for fac_score in facilities_scores:
                score_dict[fac_score.text.rstrip("\xa0")] = fac_score.find_next_sibling("span").text

            if 'Location' in score_dict:
                hotel_loc_score = float(score_dict['Location'])
            else:
                hotel_loc_score = None
            print(f'location socre: {hotel_loc_score}')

            if 'Staff' in score_dict:
                staff_score = float(score_dict['Staff'])
            else:
                staff_score = None
            print(f'staff score: {staff_score}')

            if 'Free WiFi' in score_dict:
                wifi_score = float(score_dict['Free WiFi'])
            else:
                wifi_score = None
            print(f'wifi_score: {wifi_score}')

            if 'Cleanliness' in score_dict:
                clean_score = float(score_dict['Cleanliness'])
            else:
                clean_score = None
            print(f'clean_score: {clean_score}')

# --------------------------------------------------------------
            rs_hotel_facilities = requests.get(url, headers=CFG.HEADERS)

            soup = BeautifulSoup(rs_hotel_facilities.text, "html.parser")
            facilities = soup.find('div', class_='hotel-facilities__list')
            facilities_list = [facility.text.split('\n') for facility in facilities]
            facilities_list = sum(facilities_list, [])
            if 'Non-smoking rooms' in facilities_list:
                non_smoking = True
            else:
                non_smoking = False
            print(f'non smoke: {non_smoking}')

            if 'Business centre' in facilities_list:
                business_center = True
            else:
                business_center = False
            print(f'business cent: {business_center}')

            if 'Free parking' in facilities_list:
                free_parking = True
            else:
                free_parking = False
            print(f'parking: {free_parking}')

            if '24-hour front desk' in facilities_list:
                front_desk_24_7 = True
            else:
                front_desk_24_7 = False
            print(f'24 7: {front_desk_24_7}')

            if 'Laundry' in facilities_list:
                laundry = True
            else:
                laundry = False
            print(f'Laundry: {laundry}')

            if 'Airport shuttle' in facilities_list:
                shuttle = True
            else:
                shuttle = False
            print(f'shuttle: {shuttle}')




# --------------------------------------------------------------

            dict_rows.append({'hotel_name': name, 'area': area, 'city': city,
                              'price': price, 'score': score, 'reviews': reviews,
                              'hotel_loc_score': hotel_loc_score, 'staff_score': staff_score,
                              'wifi_score': wifi_score, 'clean_score': clean_score,
                              'non_smoking': non_smoking, 'business_center': business_center,
                              'free_parking': free_parking, 'front_desk_24_7': front_desk_24_7,
                              'laundry': laundry, 'shuttle': shuttle
                               })
            # print(f'dict: {dict_rows}')


    return dict_rows

