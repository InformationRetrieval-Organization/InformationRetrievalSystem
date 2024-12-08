from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma
from aiocache import cached, SimpleMemoryCache
from aiocache.serializers import PickleSerializer


cache = SimpleMemoryCache()

@cached(ttl=None, cache=SimpleMemoryCache, serializer=PickleSerializer(), key="get_all_processed_posts")
async def get_all_processed_posts() -> List[models.Processed_Post]:
    """
    Fetch all processed_posts from the database
    """
    try:
        async with Prisma() as db:
            return await db.processed_post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching processed_posts: {e}")
        return []


async def create_one_processed_post(id: int, content: str) -> models.Processed_Post:
    """
    Create a processed_post in the database
    """
    try:
        async with Prisma() as db:
            processed_post = await db.processed_post.create(data={"id": id, "content": content})
        
            # invalidate the cache
            await cache.delete('get_all_processed_posts')

            return processed_post
    except Exception as e:
        print(f"An error occurred while creating the processed_post: {e}")


async def create_many_processed_posts(
    processed_posts: List[Dict[str, Union[int, str]]]
) -> List[models.Processed_Post]:
    """
    Create multiple processed_posts in the database
    """
    try:
        async with Prisma() as db:
            result = await db.processed_post.create_many(data=processed_posts)
            
            # invalidate the cache
            await cache.delete('get_all_processed_posts')

            return result
    except Exception as e:
        print(f"An error occurred while creating the processed_posts: {e}")


async def delete_all_processed_posts() -> None:
    """
    Delete all processed_posts from the database and reset the auto-increment counter
    """
    print("Deleting all processed_posts")

    try:
        async with Prisma() as db:
            await db.processed_post.delete_many()

            # Truncate the table and reset the ID sequence
            await db.execute_raw('TRUNCATE TABLE "Processed_Post" RESTART IDENTITY')
    except Exception as e:
        print(f"An error occurred while deleting processed_posts: {e}")
