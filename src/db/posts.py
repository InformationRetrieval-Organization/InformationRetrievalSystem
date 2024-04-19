from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma
from aiocache import cached, SimpleMemoryCache
from aiocache.serializers import PickleSerializer


cache = SimpleMemoryCache()

@cached(ttl=None, cache=SimpleMemoryCache, serializer=PickleSerializer(), key="get_all_posts")
async def get_all_posts() -> List[models.Post]:
    """
    Fetch all posts from the database
    """
    try:
        async with Prisma() as db:
            return await db.post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")
        return []


async def create_many_posts(
    posts: List[Dict[str, Union[str, datetime]]]
) -> List[models.Post]:
    """
    Create multiple posts in the database
    """
    try:
        async with Prisma() as db:
            result = await db.post.create_many(data=posts)
            
            # invalidate the cache
            await cache.delete('get_all_posts')

            return result
    except Exception as e:
        print(f"An error occurred while creating the posts: {e}")


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
        async with Prisma() as db:
            post = await db.post.create(
                data={
                    "title": title,
                    "content": content,
                    "published_on": published_on,
                    "link": link,
                    "source": source,
                }
            )

            # invalidate the cache
            await cache.delete('get_all_posts')

            return post
    except Exception as e:
        print(f"An error occurred while creating the post: {e}")


async def delete_all_posts() -> None:
    """
    Delete all posts from the database and reset the auto-increment counter
    """
    print("Deleting all posts")

    try:
        async with Prisma() as db:
            await db.post.delete_many()

            # Truncate the table and reset the ID sequence
            await db.execute_raw('TRUNCATE TABLE "Post" RESTART IDENTITY')
    except Exception as e:
        print(f"An error occurred while deleting posts: {e}")
