import os
from pynytimes import NYTAPI
import asyncio
from prisma import Prisma
from datetime import datetime
from db.posts import get_all_posts, create_post

async def main() -> None:
    prisma = Prisma()
    await prisma.connect()

    nyt_api_key = os.getenv("NYT_API_KEY")
    nyt = NYTAPI(nyt_api_key, parse_dates=True)
    begin_date = datetime.strptime("2024-03-01", "%Y-%m-%d").date()
    end_date = datetime.strptime("2024-04-01", "%Y-%m-%d").date()

    # ['abstract', 'web_url', 'snippet', 'lead_paragraph', 'print_section', 'print_page', 'source', 'multimedia', 'headline', 'keywords', 'pub_date', 'document_type', 'news_desk', 'section_name', 'subsection_name', 'byline', 'type_of_material', '_id', 'word_count', 'uri']
    articles = nyt.article_search(query="korea", 
                                dates={"begin": begin_date, "end": end_date}, 
                                results=10)

    for article in articles:
        await create_post(
            prisma, 
            article["headline"]["main"], 
            article["abstract"], 
            article["pub_date"], 
            article["web_url"]
        )

    # Get all posts
    posts = await get_all_posts(prisma)
    for post in posts:
        print(post)

    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())