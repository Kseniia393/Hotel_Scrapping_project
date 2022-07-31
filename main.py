from write_to_db import write_to_db
import time
import argparse
import conf as CFG


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--city", default="Tel Aviv")
    parser.add_argument('-i', "--check_in_date", default="2022-12-31")
    parser.add_argument('-o', "--check_out_date", default="2023-01-01")
    parser.add_argument('-a', "--adults", default="2")
    parser.add_argument('-p', "--password")
    args = parser.parse_args()
    CFG.city = args.city
    CFG.check_in_date = args.check_in_date
    CFG.check_out_date = args.check_out_date
    CFG.adults = args.adults
    CFG.PASSWORD = args.password

    write_to_db(CFG.city, CFG.check_in_date, CFG.check_out_date, CFG.adults, CFG.PASSWORD)


start_time = time.time()
if __name__ == '__main__':
    main()
print("--- %s seconds ---" % (time.time() - start_time))