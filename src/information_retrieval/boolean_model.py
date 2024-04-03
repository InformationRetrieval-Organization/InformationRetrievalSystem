from sklearn.feature_extraction.text import TfidfVectorizer
from prisma import Prisma
from db.posts import get_all_posts, create_post
import asyncio

async def build_boolean_model():
    prisma_client = Prisma()
    await prisma_client.connect()

    # Get all posts content
    posts_content = await get_all_posts(prisma_client).values_list("content", flat=True)
    
    # Tokenize the content + Map the content to the post_id
    
    # Create the Postinglists
    
    
    await prisma_client.disconnect()