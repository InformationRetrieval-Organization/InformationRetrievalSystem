import asyncio
from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_posts() -> List[models.Post]:
    """
    Fetch all posts from the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")
        return []
    finally:
        await client.disconnect()


async def create_many_posts(
    posts: List[Dict[str, Union[str, datetime]]]
) -> List[models.Post]:
    """
    Create multiple posts in the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.post.create_many(data=posts)
    except Exception as e:
        print(f"An error occurred while creating the posts: {e}")
    finally:
        await client.disconnect()


async def create_one_post(
    title: str,
    content: str,
    published_on: datetime,
    link: str,
    source: str,
) -> models.Post:
    """
    Create a post in the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.post.create(
            data={
                "title": title,
                "content": content,
                "published_on": published_on,
                "link": link,
                "source": source,
            }
        )
    except Exception as e:
        print(f"An error occurred while creating the post: {e}")
    finally:
        await client.disconnect()


async def delete_all_posts() -> None:
    """
    Delete all posts from the database
    """
    print("Deleting all posts")

    try:
        client = Prisma()
        await client.connect()

        await client.post.delete_many()
    except Exception as e:
        print(f"An error occurred while deleting posts: {e}")
    finally:
        await client.disconnect()
