import requests
import pandas as pd
import os
from datetime import datetime
import time
from data_crawlers.helper import write_to_csv

def get_gnews_api_key():
    return os.getenv("GNEWS_API_KEY")

def get_file_path():
    cwd = os.getcwd()
    return os.path.join(cwd, 'files', 'GNews.csv')

def get_gnews_data(api_key, begin_date, end_date, page):
    url = "https://gnews.io/api/v4/search"
    params = {
        "apikey": api_key,
        "from": begin_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "to": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "q": "korea",
        #"country": "us",
        "max": 50, # this is the maximum
        "expand": "content",
        "page": page
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return None

def crawl_gnews_data() -> None:
    gnews_api_key = get_gnews_api_key()
    begin_date = datetime.strptime("20240301", "%Y%m%d").date()
    end_date = datetime.strptime("20240410", "%Y%m%d").date()
    file_path = get_file_path()

    if os.path.exists(file_path):
        os.remove(file_path)

    page = 1
    while True:
        articles = get_gnews_data(gnews_api_key, begin_date, end_date, page)
        if not articles:
            break

        data = []
        for article in articles:
            data.append({
                'title': article["title"],
                #'description': article["description"],
                'content': article["content"],
                #'url': article["url"],
                #'image': article["image"],
                'published_on': article["publishedAt"],
                #'source_name': article["source"]["name"],
                'link': article["source"]["url"],
                'source': article["source"]["name"]
            })

        write_to_csv(file_path, data)

        page += 1

        # Pause for 0.2 second to avoid exceeding the rate limit of 6 requests per second
        time.sleep(0.2)

if __name__ == "__main__":
    crawl_gnews_data()