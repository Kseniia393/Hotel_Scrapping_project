from get_urls import get_urls
import conf as CFG

url_search = CFG.URL0
for i in get_urls(url_search):
    print(i)