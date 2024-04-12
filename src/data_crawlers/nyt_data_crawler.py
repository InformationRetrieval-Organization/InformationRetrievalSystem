import os
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import asyncio
from helper import *


async def crawl_nyt_data() -> None:
    nyt_api_key = get_nyt_api_key()
    begin_date = get_crawl_start_date()
    end_date = get_crawl_end_date()
    file_path = get_nyt_file_path()

    print("Crawling New York Times data...")
    print(f"Begin date: {begin_date}")
    print(f"End date: {end_date}")

    if os.path.exists(file_path):
        os.remove(file_path)

    driver = login_nyt()

    # because there is a limit of 10 articles per page, we need to loop through all pages
    page = 1
    total_articles = 0
    while True:
        articles = get_articles(query="korea",
                                begin_date=begin_date, 
                                end_date=end_date, 
                                api_key=nyt_api_key, 
                                page=page)
        if not articles:
            break

        data = []
        for article in articles:
            full_text = get_full_article(article["web_url"], driver)
            published_on = datetime.fromisoformat(article["pub_date"])   

            data.append({
                'title': article["headline"]["main"], 
                'content': full_text, 
                'published_on': published_on,
                'link': article["web_url"],
                'source': "New York Times"
            })   

        write_to_csv(file_path, data)

        total_articles += len(data)
        page += 1

    print(f"Total articles retrieved: {total_articles}")
    driver.quit()


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

def get_full_article(url, driver):
    # Use the provided webdriver to access the logged-in session
    driver.get(url)
      
    # Wait up to 10 seconds for the body tag to appear
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "articleBody")))
    except TimeoutException:
        print(f"TimeoutException: Element with tag name 'articleBody' not found on {url}")
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the HTML from the webdriver

    article_body = soup.find('section', {'name': 'articleBody'})

    if article_body:
        full_text = ' '.join([p.get_text() for p in article_body.find_all('p')])
        unwanted_text = "Open this article in the New York Times Audio app on iOS. Subscribe to The Times to read as many articles as you like."
        full_text = full_text.replace(unwanted_text, "")
        return full_text
    else:
        return None

def login_nyt():
    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://myaccount.nytimes.com/auth/login")

    # uncomment this for automatic login, but i got blocked by NYT for too many requests
    '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    email_input = driver.find_element("name", "email")
    email_input.clear()
    email_input.send_keys(os.getenv("NYT_EMAIL"))

    # If there's a login button you can click it like this:
    continue_button = driver.find_element(By.XPATH, '//button[normalize-space()="Continue"]')
    continue_button.click()

    # Wait up to 10 seconds for the password field to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

    # If there's a password field, you can fill it in a similar way:
    password_input = driver.find_element("name", "password")
    password_input.clear()
    password_input.send_keys(os.getenv("NYT_PASSWORD"))

    continue_button = driver.find_element(By.XPATH, '//button[normalize-space()="Log In"]')
    continue_button.click()
    '''

    # Pause the script until the user presses Enter
    input("Press Enter after you have completed the verification...")

    return driver

if __name__ == "__main__":
    asyncio.run(crawl_nyt_data())