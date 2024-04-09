import requests
import asyncio
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def get_guardian_api_key():
    return os.getenv("GUARDIAN_API_KEY")

def get_file_path():
    cwd = os.getcwd()
    return os.path.join(cwd, 'files', 'The Guardian.csv')

def get_guardian_data(guardian_api_key, begin_date, end_date):
    url = "https://content.guardianapis.com/search"
    params = {
        "api-key": guardian_api_key,
        "from-date": begin_date.strftime("%Y-%m-%d"),
        "to-date": end_date.strftime("%Y-%m-%d"),
        "q": "korea",
    }
    return requests.get(url, params=params)

def get_full_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    article_body = soup.find('div', {'id': 'maincontent'})

    return ' '.join([p.get_text() for p in article_body.find_all('p')]) if article_body else None

def write_to_csv(file_path, articles):
    df = pd.DataFrame(articles)
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

async def crawl_guardian_data() -> None:
    guardian_api_key = get_guardian_api_key()
    begin_date = datetime.strptime("20240401", "%Y%m%d").date()
    end_date = datetime.strptime("20240410", "%Y%m%d").date()
    file_path = get_file_path()

    if os.path.exists(file_path):
        os.remove(file_path)

    response = get_guardian_data(guardian_api_key, begin_date, end_date)

    if response.status_code == 200:
        data = response.json()
        articles = []
        for result in data["response"]["results"]:
            article_url = result["webUrl"]
            full_text = get_full_article(article_url)
            articles.append({
                'title': result["webTitle"],
                'content': full_text,
                'published_on': result["webPublicationDate"],
                'link': article_url
            })
        write_to_csv(file_path, articles)
    else:
        return None

if __name__ == "__main__":
    asyncio.run(crawl_guardian_data())