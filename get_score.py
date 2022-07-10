from bs4 import BeautifulSoup
from get_batch_response import get_batch_response
from get_urls import get_urls

#IMPORTANT!! NEEDS TO BE RE-DONE
# def get_score():
#     url_list = get_urls()
#     response = get_batch_response(url_list)
#
#     name_list = []
#     for rs in response:
#         soup = BeautifulSoup(rs.text, "html.parser")
#         name = soup.find_all("div", class_="fcab3ed991 a23c043802")
#         for n in name:
#             name_list.append(n.text)
#     print(len(name_list))
#
#     score_list = []
#     for rs in response:
#         soup = BeautifulSoup(rs.text, "html.parser")
#         score = soup.find_all("div", class_="b5cd09854e d10a6220b4")
#         for sc in score:
#             score_list.append(sc.text)
#     print(len(score_list))



print(get_score())