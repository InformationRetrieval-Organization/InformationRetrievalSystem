import pandas as pd
from db.posts import create_many_posts, delete_all_posts, get_all_posts
from db.processed_posts import delete_all_processed_posts
import os
from dateutil.parser import parse
import glob
from config import GNEWS_FILE_PATH, GUARDIAN_FILE_PATH


async def init_database():
    """
    Initialize the database by deleting the existing posts and processed_posts and inserting the articles from the files into the database
    """

    # Get all posts from the database
    posts = await get_all_posts()

    print(f"Initial length of posts in database: {len(posts)}")

    # If there are no posts in the database, delete and insert posts
    if not posts:
        await delete_all_posts()
        await delete_all_processed_posts()
        await insert_file_posts()


async def insert_file_posts():
    """
    Insert articles from files into the database
    """
    print("Inserting articles from files into the database")

    csv_files = [GNEWS_FILE_PATH, GUARDIAN_FILE_PATH]

    all_posts = []

    # Iterate over all CSV files
    for file_path in csv_files:
        # check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path)

        # Iterate over the DataFrame and add each row to the all_posts list
        for _, row in df.iterrows():
            published_on = parse(row["published_on"])
            content = row["content"]
            if pd.isnull(content):  # Check if content is NaN
                content = None  # Convert NaN to None
            elif not isinstance(content, str):  # Check if content is not a string
                content = str(content)  # Convert content to a string

            all_posts.append(
                {
                    "title": row["title"],
                    "content": content,
                    "published_on": published_on,
                    "link": row["link"],
                    "source": row["source"],
                }
            )

        print(f"Read {len(all_posts)} articles from {file_path}")

    # Insert all posts into the database at once
    await create_many_posts(all_posts)

    print(f"Inserted {len(all_posts)} articles into the database")
