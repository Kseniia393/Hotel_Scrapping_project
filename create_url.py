def create_url(city='Tel-Aviv', country='Israel', date_in='2022-12-31', date_out='2023-01-01', off_set=0):
    """
    Function create one url with city, country, check in date and check out date, number of page.
    :param city: city where want to find hotel
    :param country: country where want to find hotel
    :param date_in: check in date where want to find hotel
    :param date_out: check out date where want to find hotel
    :param off_set: number of searching page (be contained without remainder on 25)
    :return: url with parameters (default it is Tel-Aviv, Israel, 2022-12-31 - 2023-01-01, the first page of searching)
    """
    count_people = 2
    url = "https://www.booking.com/searchresults.html?" \
          "checkin={check_in}" \
          "&checkout={check_out}" \
          "&group_adults={group_adults}" \
          "&group_children=0&order=score" \
          "&ss={city}%2C%20{country}" \
          "&selected_currency=USD" \
          "&offset={limit}".format(
            check_in=date_in,
            check_out=date_out,
            group_adults=count_people,
            country=country,
            limit=off_set,
            city=city)
    return url
