import requests
import asyncio
import os
from bs4 import BeautifulSoup
from helper import *


def get_guardian_data(api_key: str, begin_date: date, end_date: date, page: int = 1):
    """
    Get news articles from The Guardian API.
    """
    url = "https://content.guardianapis.com/search"
    params = {
        "api-key": api_key,
        "from-date": begin_date.strftime("%Y-%m-%d"), # YYYY-MM-DD
        "to-date": end_date.strftime("%Y-%m-%d"), # YYYY-MM-DD
        "use-date": "published",
        "order-by": "newest",
        "page-size": 10, # this is the maximum
        "q": "korea",
        "page": page,
    }
    return requests.get(url, params=params)


def get_full_article(url):
    """
    Get the full text of a news article from The Guardian.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get page: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    article_body = soup.find("div", {"id": "maincontent"})

    return (
        " ".join([p.get_text() for p in article_body.find_all("p")])
        if article_body
        else None
    )


async def crawl_guardian_data() -> None:
    """
    Crawl news articles from The Guardian API and save them to a CSV file.
    """
    guardian_api_key = get_guardian_api_key()
    begin_date = get_crawl_start_date()
    end_date = get_crawl_end_date()
    file_path = get_guardian_file_path()

    print("Crawling The Guardian data...")
    print(f"Begin date: {begin_date}")
    print(f"End date: {end_date}")

    if os.path.exists(file_path):
        os.remove(file_path)

    page = 1
    total_articles = 0
    while True:
        response = get_guardian_data(
            api_key=guardian_api_key,
            begin_date=begin_date,
            end_date=end_date,
            page=page,
        )

        if response.status_code == 200:
            data = response.json()
            if not data["response"]["results"]:
                break

            articles = []
            for result in data["response"]["results"]:
                article_url = result["webUrl"]
                full_text = get_full_article(article_url)
                articles.append(
                    {
                        "title": result["webTitle"],
                        "content": full_text,
                        "published_on": result["webPublicationDate"],
                        "link": article_url,
                        "source": "The Guardian",
                    }
                )
            write_to_csv(file_path, articles)

            total_articles += len(articles)
            page += 1
        else:
            break

    print(f"Total articles retrieved: {total_articles}")


if __name__ == "__main__":
    asyncio.run(crawl_guardian_data())
