import asyncio
from datetime import datetime
from typing import Dict, List, Union
from prisma import models
from prisma import Prisma


async def get_all_processed_posts() -> List[models.Processed_Post]:
    """
    Fetch all processed_posts from the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.processed_post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching processed_posts: {e}")
        return []
    finally:
        await client.disconnect()


async def create_one_processed_post(id: int, content: str) -> models.Processed_Post:
    """
    Create a processed_post in the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.processed_post.create(data={"id": id, "content": content})
    except Exception as e:
        print(f"An error occurred while creating the processed_post: {e}")
    finally:
        await client.disconnect()


async def create_many_processed_posts(
    processed_posts: List[Dict[str, Union[int, str]]]
) -> List[models.Processed_Post]:
    """
    Create multiple processed_posts in the database
    """
    try:
        client = Prisma()
        await client.connect()

        return await client.processed_post.create_many(data=processed_posts)
    except Exception as e:
        print(f"An error occurred while creating the processed_posts: {e}")
    finally:
        await client.disconnect()


async def delete_all_processed_posts() -> None:
    """
    Delete all processed_posts from the database
    """
    print("Deleting all processed_posts")

    try:
        client = Prisma()
        await client.connect()

        await client.processed_post.delete_many()
    except Exception as e:
        print(f"An error occurred while deleting processed_posts: {e}")
    finally:
        await client.disconnect()
