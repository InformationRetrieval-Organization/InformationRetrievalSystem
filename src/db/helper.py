import pandas as pd
from db.posts import create_many_posts, delete_all_posts
from db.processed_posts import delete_all_processed_posts
import os
from dateutil.parser import parse
import glob


async def init_database():
    """
    Initialize the database by deleting the existing posts and processed_posts and inserting the articles from the files into the database
    """

    await delete_all_posts()
    await delete_all_processed_posts()
    await insert_posts()


async def insert_posts():
    """
    Insert articles from files into the database
    """
    print("Inserting articles from files into the database")
    cwd = os.getcwd()
    files_path = os.path.join(cwd, "files", "*.csv")

    # Get all CSV files in the directory
    csv_files = glob.glob(files_path)

    # Iterate over all CSV files
    for file_path in csv_files:
        # check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path)

        posts = []
        # Iterate over the DataFrame and insert each row into the database
        for _, row in df.iterrows():
            published_on = parse(row["published_on"])
            content = row["content"]
            if pd.isnull(content):  # Check if content is NaN
                content = None  # Convert NaN to None
            elif not isinstance(content, str):  # Check if content is not a string
                content = str(content)  # Convert content to a string

            posts.append(
                {
                    "title": row["title"],
                    "content": content,
                    "published_on": published_on,
                    "link": row["link"],
                    "source": row["source"],
                }
            )

        await create_many_posts(posts)
