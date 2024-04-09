import asyncio
from datetime import datetime
from prisma import models
from db.decorators import inject_service_provider
from db.service_provider import ServiceProvider


@inject_service_provider
async def get_all_processed_posts(
    service_provider: ServiceProvider,
) -> list[models.Processed_Post]:
    """
    Fetch all processed_posts from the database
    """
    try:
        prisma = await service_provider.get_prisma()
        return await prisma.processed_post.find_many()
    except Exception as e:
        print(f"An error occurred while fetching processed_posts: {e}")


@inject_service_provider
async def create_processed_post(
    service_provider: ServiceProvider, id: int, content: str
) -> models.Processed_Post:
    """
    Create a processed_post in the database
    """
    try:
        prisma = await service_provider.get_prisma()
        return await prisma.processed_post.create(data={"id": id, "content": content})
    except Exception as e:
        print(f"An error occurred while creating the processed_post: {e}")


@inject_service_provider
async def delete_processed_posts(service_provider: ServiceProvider) -> None:
    """
    Delete all processed_posts from the database
    """
    print("Deleting all processed_posts")

    try:
        prisma = await service_provider.get_prisma()
        await prisma.processed_post.delete_many()
    except Exception as e:
        print(f"An error occurred while deleting processed_posts: {e}")
