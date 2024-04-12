import requests
import pandas as pd
import os
import time
from helper import *


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
    begin_date = get_crawl_start_date()
    end_date = get_crawl_end_date()
    file_path = get_gnews_file_path()

    print("Crawling GNews data...")
    print(f"Begin date: {begin_date}")
    print(f"End date: {end_date}")

    if os.path.exists(file_path):
        os.remove(file_path)

    page = 1
    total_articles = 0
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

        total_articles += len(data)
        page += 1

        # Pause for 0.2 second to avoid exceeding the rate limit of 6 requests per second
        time.sleep(0.2)

    print(f"Total articles retrieved: {total_articles}")

if __name__ == "__main__":
    crawl_gnews_data()