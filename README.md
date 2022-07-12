## BOOKING scrapping 
### data mining project for ITC
<p align="center">
<img src="img/ITC_logo.png" width=150></p>

> Finding - Parsing - Analysis

This program parsing booking.com. By creating  link according to transmitted request date. Parsing page, getting important information about hotel. Save it to *.csv file. Programe made by Kseniia Konoshko, Anna Lelchuk, Alexey Konev during ITC june 2022 Data Science cohort.

### How to run it
- Download __*.zip__ file
- Unzip it at any suitable folder
- Install all libs from __requirements.txt__
- Run __main.py__
- That's all
```bash
pip install -r requirements.txt
python main.py
```
### Structure of files
- __[venv]__ - environment folder
- __conf__ - configuration file
- __requirements.txt__ - file list off all needed modules
- __main__ - primary startup file
- __get*__ and __create*__ supporting files
### Main library used
- modules __requests__ and __grequest__ helps to get response from site
- module __bs4 (Beautiful Soup)__ is probably the best library to parse information from html
- module __re__ consists most popular regular expressions 

### License
Totally __FREE__ as Open-source. 
But it is advisable to use (c) ITC by Kseniia Konoshko, Anna Lelchuk, Alexey Konev
### Functionality of functions
| *Function*           | *What do and return*                                                                                                                                                                    |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| crete_url            | Function create one url with city, country, check in date and check out date, number of page.<br/>**return:** url                                                                       |
| get_urls             | Function generate all pages of the same search<br/>**return:** list of urls of all pages in the search                                                                                  |
| create_dict_rows     | Create d dictionary that represent by itself a row of a future table.As a key we use names of the columns.<br/>**return:** list of dictionaries                                         |
| get_total_hotel_nums | Function parse on the url amd find number of all hotels according to transmitted request date. Use this value to create offset number.<br/>**return:** integer number of all hotels |
| get_soup             | Function return soup by url<br/>**return:** soup                                                                                                                                        |
| write_to_csv         | Function write to csv file all data as a table                                                                                                                                          |

