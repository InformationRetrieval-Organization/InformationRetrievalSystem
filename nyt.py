from pynytimes import NYTAPI

nyt = NYTAPI("RGZ1tQCYoZxIDgjsFgVKTf2dTSwNRAsk", parse_dates=True)

articles = nyt.article_search(query="korea")

print(articles)
