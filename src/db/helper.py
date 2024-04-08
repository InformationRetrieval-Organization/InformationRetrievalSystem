from db.posts import delete_posts

async def init_database():
    return await delete_posts()