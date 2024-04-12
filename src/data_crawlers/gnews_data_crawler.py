import requests
import os
import time as t
from helper import *


def get_gnews_data(api_key: str, begin_date: date, end_date: date, page: int = 1):
    """
    Get news articles from GNews API.
    """
    url = "https://gnews.io/api/v4/search"
    params = {
        "apikey": api_key,
        "from": begin_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "to": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "q": "korea",
        # "country": "us",
        # "lang": "en",
        "max": 100,  # this is the maximum
        "expand": "content",
        "sortby": "publishedAt",  # "relevance", "publishedAt
        "page": page,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return None


def crawl_gnews_data() -> None:
    """
    Crawl news articles from GNews API and save them to a CSV file.
    """
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
        articles = get_gnews_data(
            api_key=gnews_api_key, begin_date=begin_date, end_date=end_date, page=page
        )
        if not articles:
            break

        data = []
        for article in articles:
            data.append(
                {
                    "title": article["title"],
                    "content": article["content"],
                    "published_on": article["publishedAt"],
                    "link": article["source"]["url"],
                    "source": article["source"]["name"],
                }
            )

        write_to_csv(file_path, data)

        total_articles += len(data)
        page += 1

        # Pause for 0.2 second to avoid exceeding the rate limit of 6 requests per second
        t.sleep(0.2)

    print(f"Total articles retrieved: {total_articles}")


if __name__ == "__main__":
    crawl_gnews_data()
