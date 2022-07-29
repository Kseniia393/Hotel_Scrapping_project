import csv
from create_dict_rows import create_dict_rows
import re
import time
#fake-useragent


def main():
    create_dict_rows()


start_time = time.time()
if __name__ == '__main__':
    main()
print("--- %s seconds ---" % (time.time() - start_time))