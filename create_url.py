import argparse

def create_url(off_set=0):
    """
    Function creates the initial url for hotel search.
    Parameters city, check in date and check out date, number of travelers is received from user input
    :param off_set: number of searching page (be contained without remainder on 25)
    :return: url with first page of searching
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--city", default="TelAviv")
    parser.add_argument('-i', "--date_in", default="2022-12-31")
    parser.add_argument('-o', "--date_out", default="2023-01-01")
    parser.add_argument('-p', "--count_people", default="2")

    args = parser.parse_args()

    city = args.city
    city = city.replace(" ", "")
    date_in = args.date_in
    date_out = args.date_out
    count_people = args.count_people

    # city = input("Enter the city where you want to travel to, e.g. 'Tel Aviv': ")
    # city = city.replace(" ", "")
    # date_in = input("Enter check-in date in format yyyy-mm-dd: ")
    # date_out = input("Enter check-out date in format yyyy-mm-dd: ")
    # count_people = input("Enter the number of people traveling: ")

    url = "https://www.booking.com/searchresults.html?" \
          "checkin={check_in}" \
          "&checkout={check_out}" \
          "&group_adults={group_adults}" \
          "&group_children=0&order=score" \
          "&ss={city}" \
          "&selected_currency=USD" \
          "&offset={limit}".format(
        check_in=date_in,
        check_out=date_out,
        group_adults=count_people,
        limit=off_set,
        city=city)
    return url
