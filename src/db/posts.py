import os
import asyncio
from prisma import Prisma
from datetime import datetime

async def get_all_posts(prisma) -> list[any]:
    try:
        return await prisma.post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")

async def create_post(prisma, title, content, published_on, link):
    try:
        return await prisma.post.create(
            data = {
                "title": title,
                "content": content,
                "published_on": published_on,
                "link": link,
            }
        )
    except Exception as e:
        print(f"An error occurred while creating the post: {e}")