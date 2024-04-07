import os
import asyncio
from datetime import datetime
from singleton.prisma_singleton import PrismaSingleton
from prisma import models

prisma = PrismaSingleton().db

async def get_all_posts() -> list[models.Post]:
    try:
        return await prisma.post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")

async def create_post(title, content, published_on, link) -> models.Post:
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
