def create_url(city='Tel-Aviv', country='Israel', off_set=0, date_in='2022-12-31', date_out='2023-01-01'):
    count_people = 2
    url = "https://www.booking.com/searchresults.html?" \
          "checkin={check_in}" \
          "&checkout={check_out}" \
          "&group_adults={group_adults}" \
          "&group_children=0&order=score" \
          "&ss={city}%2C%20{country}" \
          "&selected_currency=NIS" \
          "&offset={limit}".format(
            check_in=date_in,
            check_out=date_out,
            group_adults=count_people,
            country=country,
            limit=off_set,
            city=city)
    return url
