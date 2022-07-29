import argparse


def create_url(off_set=0):
    """
    Function creates the initial url for hotel search.
    Arguments city (-c), check in date (-i), check out date (-o), number of people (-p) are parsed from the CLI.
    Default arguments: telaviv 2022-12-31 2023-01-01 2
    :param off_set: number of searching page (be contained without remainder on 25)
    :return: url with first page of searching
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--city", default="Tel Aviv")
    parser.add_argument('-i', "--check_in_date", default="2022-12-31")
    parser.add_argument('-o', "--check_out_date", default="2023-01-01")
    parser.add_argument('-p', "--adults", default="2")

    args = parser.parse_args()

    city = args.city
    city = city.replace(" ", "")
    check_in_date = args.check_in_date
    check_out_date = args.check_out_date
    adults = args.adults

    # city = input("Enter the city where you want to travel to, e.g. 'Tel Aviv': ")
    # city = city.replace(" ", "")
    # check_in_date = input("Enter check-in date in format yyyy-mm-dd: ")
    # check_out_date = input("Enter check-out date in format yyyy-mm-dd: ")
    # adults = input("Enter the number of people traveling: ")

    url = "https://www.booking.com/searchresults.html?" \
          "checkin={check_in}" \
          "&checkout={check_out}" \
          "&group_adults={group_adults}" \
          "&group_children=0&order=score" \
          "&ss={city}" \
          "&selected_currency=USD" \
          "&offset={limit}".format(
        check_in=check_in_date,
        check_out=check_out_date,
        group_adults=adults,
        limit=off_set,
        city=city)
    return url, city, check_in_date, check_out_date, adults
