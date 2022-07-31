## BOOKING scrapping 
### data mining project for ITC
<p align="center">
<img src="img/ITC_logo.png" width=150></p>

> Finding - Parsing - Analysis

This program parses booking.com by creating  link according to transmitted request date. 
<br>Parsing page, getting important information about hotel. Save it to *.csv file. 
Program made by Kseniia Konoshko, Anna Lelchuk, Alexey Konev during ITC june 2022 Data Science cohort.

### How to run it
- Download __*.zip__ file
- Unzip it at any suitable folder
- Install all libs from __requirements.txt__
- Make sure you pass as CLI argument "-p <i>\<your mysql password></i>"
- Run __main.py__
- That's all
```bash
pip install -r requirements.txt
python main.py -p MYSQL_PASSWORD
```
### Structure of files
- __[venv]__ - environment folder
- __conf__ - configuration file
- __requirements.txt__ - file list off all needed modules
- __main__ - primary startup file
- __get*__ and __create*__ supporting files
### Main library used
- modules __requests__  gets response from site
- module __bs4 (Beautiful Soup)__ is probably the best library to parse information from html
- module __re__ consists most popular regular expressions 
- module __pymysql__ performs actions on a database (create, populate)
- module __argparse__ collects arguments from CLI

### License
Totally __FREE__ as Open-source. 
But it is advisable to use (c) ITC by Kseniia Konoshko, Anna Lelchuk, Alexey Konev
### Functionality of functions
| *Function*           | *What do and return*                                                                                                                                                                |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| main                 | Parses arguments from CLI and calls function write_to_db                                                                                                                            |
| write_to_db          | Create dictionary with hotel data. Populate db tables with collected hotel details                                                                                                  |
| create_DB            | Checks if DB exists, if not creates database and tables                                                                                                                             |
| create_url           | Function create one url with city, country, check in date and check out date, number of page.<br/>**return:** url                                                                   |
| get_urls             | Function generate all pages of the same search<br/>**return:** list of urls of all pages in the search                                                                              |
| get_total_hotel_nums | Function parse on the url amd find number of all hotels according to transmitted request date. Use this value to create offset number.<br/>**return:** integer number of all hotels |

