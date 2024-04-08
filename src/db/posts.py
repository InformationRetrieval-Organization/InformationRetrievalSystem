import asyncio
from datetime import datetime
from prisma import models
from db.decorators import inject_service_provider
from db.service_provider import ServiceProvider

@inject_service_provider
async def get_all_posts(service_provider: ServiceProvider) -> list[models.Post]:
    try:
        prisma = await service_provider.get_prisma()
        return await prisma.post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")

@inject_service_provider
async def create_post(service_provider: ServiceProvider, title, content, published_on, link) -> models.Post:
    try:
        prisma = await service_provider.get_prisma()
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

@inject_service_provider
async def delete_posts(service_provider: ServiceProvider) -> None:
    try:
        prisma = await service_provider.get_prisma()
        await prisma.post.delete_many()
    except Exception as e:
        print(f"An error occurred while deleting posts: {e}")
