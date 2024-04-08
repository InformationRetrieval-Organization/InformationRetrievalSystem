import os
import asyncio
from datetime import datetime
from db.posts import get_all_posts, create_post
import requests
import json


async def crawl_nyt_data() -> None:
    nyt_api_key = os.getenv("NYT_API_KEY")
    begin_date = datetime.strptime("20240301", "%Y%m%d").date()
    end_date = datetime.strptime("20240401", "%Y%m%d").date()

    # because there is a limit of 10 articles per page, we need to loop through all pages
    page = 1
    while True:
        articles = get_articles(query="korea", 
                                begin_date=begin_date, 
                                end_date=end_date, 
                                api_key=nyt_api_key, 
                                page=page)
        if not articles:
            break

        for article in articles:
            await create_post(
                title=article["headline"]["main"], 
                content=article["abstract"], 
                published_on=datetime.fromisoformat(article["pub_date"]),
                link=article["web_url"]
            )

        page += 1

    """
    # print all posts
    posts = await get_all_posts()
    for post in posts:
        print(post) 
    """


def get_articles(query, begin_date, end_date, api_key, page=1):
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": query,
        "begin_date": begin_date,
        "end_date": end_date,
        "api-key": api_key,
        "page": page
    }

    # limit of 1 request per minute and 500 per day
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["response"]["docs"]
    else:
        return None