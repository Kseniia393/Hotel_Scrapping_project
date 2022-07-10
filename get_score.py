# from bs4 import Beautiful
from get_batch_response import get_batch_response
from get_urls import get_urls


def get_score():
    url_list = get_urls()
    response = get_batch_response(url_list)
    score_list = []
    for rs in response:
        soup = BeautifulSoup(rs.text, "html.parser")
        score = soup.find_all("div", class_="b5cd09854e d10a6220b4")
        # score_list.append(score)
    return score_list

print(get_score())