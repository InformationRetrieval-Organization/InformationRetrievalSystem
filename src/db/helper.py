import pandas as pd
from db.posts import create_post, delete_posts
from db.processed_posts import delete_processed_posts
import os
from datetime import datetime

async def init_database():
    await delete_posts()
    await delete_processed_posts()
    await insert_posts()

async def insert_posts():
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'files', 'Post.csv')

    # check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    # Iterate over the DataFrame and insert each row into the database
    for _, row in df.iterrows():
        published_on = datetime.strptime(row['published_on'], "%Y-%m-%d %H:%M:%S")
        content = row['content']
        if pd.isnull(content):  # Check if content is NaN
            content = None  # Convert NaN to None
        elif not isinstance(content, str):  # Check if content is not a string
            content = str(content)  # Convert content to a string
        await create_post(title=row['title'], content=content, published_on=published_on, link=row['link'])