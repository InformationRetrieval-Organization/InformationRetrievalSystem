import asyncio
from datetime import datetime
from prisma import models
from db.decorators import inject_service_provider
from db.service_provider import ServiceProvider

@inject_service_provider
async def get_all_posts(service_provider: ServiceProvider) -> list[models.Processed_Post]:
    try:
        prisma = await service_provider.get_prisma()
        return await prisma.processed_post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")

@inject_service_provider
async def create_post(service_provider: ServiceProvider, id: int, content: str) -> models.Processed_Post:
    try:
        prisma = await service_provider.get_prisma()
        return await prisma.processed_post.create(
            data = {
                "id": id,
                "content": content
            }
        )
    except Exception as e:
        print(f"An error occurred while creating the post: {e}")

@inject_service_provider
async def delete_posts(service_provider: ServiceProvider) -> None:
    try:
        prisma = await service_provider.get_prisma()
        await prisma.processed_post.delete_many()
    except Exception as e:
        print(f"An error occurred while deleting posts: {e}")
