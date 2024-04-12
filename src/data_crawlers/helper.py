from datetime import date, datetime
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def write_to_csv(file_path, articles):
    """
    Append articles to a CSV file
    """
    df = pd.DataFrame(articles)
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

def get_nyt_api_key() -> str:
    return os.getenv("NYT_API_KEY")

def get_guardian_api_key():
    return os.getenv("GUARDIAN_API_KEY")

def get_gnews_api_key():
    return os.getenv("GNEWS_API_KEY")

def get_guardian_file_path():
    cwd = os.getcwd()
    return os.path.join(cwd, 'files', 'The Guardian.csv')

def get_nyt_file_path():
    cwd = os.getcwd()
    return os.path.join(cwd, 'files', 'New York Times.csv')

def get_gnews_file_path():
    cwd = os.getcwd()
    return os.path.join(cwd, 'files', 'GNews.csv')

def get_crawl_start_date() -> date:
    return datetime.strptime(os.getenv("CRAWL_START_DATE"), "%Y-%m-%d").date()

def get_crawl_end_date() -> date:
    return datetime.strptime(os.getenv("CRAWL_END_DATE"), "%Y-%m-%d").date()

