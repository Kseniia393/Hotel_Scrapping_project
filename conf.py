

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
URL_TEST = r"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaGqIAQGYAQm4AQfIAQ3YAQPoAQGIAgGoAgO4ApfnqpYGwAIB0gIkMzRlMDJhNTItMTY3Ny00MGEzLTk2MDYtODk4NzE2NDIzOWFh2AIE4AIB&sid=9ab9d72185a104fb71ed8b3eebafb106&aid=304142&ss=Tel+Aviv&ssne=Tel+Aviv&ssne_untouched=Tel+Aviv&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-781545&dest_type=city&checkin=2022-12-31&checkout=2023-01-01&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0"
HOTELS_PER_PAGE = 25
BATCH_SIZE = 5
LOG_FILE = 'log_booking_scrap'

#password to db is collected from CLI argument:
PASSWORD = ''

#Google Engine API key is collected from CLI argument:
API_KEY = ''

# these are facilities that we are interested in.
FACILITIES = ['Non-smoking rooms', 'Business centre', 'Free parking', '24-hour front desk', 'Laundry', 'Airport shuttle']

DB_HOST = 'data-mining-db1.cttpnp4olbpx.us-west-1.rds.amazonaws.com'
DB_USER = 'alexey_anna_kseniia'
DB_NAME = 'alexey_anna_kseniia'

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password=PASSWORD,
#                              database='hotels_booking',
#                              cursorclass=pymysql.cursors.DictCursor)