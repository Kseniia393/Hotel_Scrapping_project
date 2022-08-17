import re
import requests
from bs4 import BeautifulSoup

def scrap_facilities(soup):
    """
    Scraps hotel page and gets different facilities
    :return: facilities_list
    """
    facilities = soup.find('div', class_='hotel-facilities__list')
    if facilities:
        facilities_list = [facility.text.split('\n') for facility in facilities]
        facilities_list = sum(facilities_list, [])
    else:
        facilities_list = []
    return facilities_list


def scrape_hotel(hotel_soup):
    """
    Scrap part of soup to get hotel data from the main page
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

    hotel_score = hotel_soup.findChild('div', class_='b5cd09854e d10a6220b4')
    if hotel_score is not None:
        hotel_score = hotel_score.text

    hotel_review = hotel_soup.findChild('div', class_='d8eab2cf7f c90c0a70d3 db63693c62')
    if hotel_review is not None:
        hotel_review = int(re.findall(r'\d+', hotel_review.text.replace(',', ''))[0])

    url = hotel_soup.findChild('a').get('href')
    return hotel_title, hotel_area, hotel_city, price, hotel_score, hotel_review, url


def scrap_scores(score_dict):
    """
    Scrap hotel page and get different scores: Location, Staff, Free WiFi, Cleanliness,
    if they are presented on the page
    :return: hotel_loc_score, hotel_staff_score, hotel_wifi_score, hotel_cleanliness_score
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
