from sklearn.feature_extraction.text import TfidfVectorizer
from prisma import Prisma
from db.posts import get_all_posts, create_post
import asyncio

async def build_vector_space_model():
    prisma_client = Prisma()
    await prisma_client.connect()

    # Get all posts content
    posts_content = await get_all_posts(prisma_client).values_list("content", flat=True)

    # Create the Transform
    vectorizer = TfidfVectorizer()

    # Tokenize and build vocab
    vectorizer.fit(posts_content)

    # Encode document
    vector = vectorizer.transform(posts_content)

    # Summarize encoded vector
    print("Shape:", vector.shape)
    print(vector.toarray())

    await prisma_client.disconnect()