

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
URL_TEST = r"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaGqIAQGYAQm4AQfIAQ3YAQPoAQGIAgGoAgO4ApfnqpYGwAIB0gIkMzRlMDJhNTItMTY3Ny00MGEzLTk2MDYtODk4NzE2NDIzOWFh2AIE4AIB&sid=9ab9d72185a104fb71ed8b3eebafb106&aid=304142&ss=Tel+Aviv&ssne=Tel+Aviv&ssne_untouched=Tel+Aviv&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-781545&dest_type=city&checkin=2022-12-31&checkout=2023-01-01&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0"
HOTELS_PER_PAGE = 25
BATCH_SIZE = 5

city=''
check_in_date =''
check_out_date =''
adults = ''
PASSWORD = ''

# these are facilities that we are interested in.
FACILITIES = ['Non-smoking rooms', 'Business centre', 'Free parking', '24-hour front desk', 'Laundry', 'Airport shuttle']

