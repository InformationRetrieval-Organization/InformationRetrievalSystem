# TODO: Implement the Boolean Model, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/3

from sklearn.feature_extraction.text import TfidfVectorizer
from prisma import Prisma
from db.posts import get_all_posts, create_post
from linked_list import LinkedList

async def build_boolean_model():
    prisma_client = Prisma()
    await prisma_client.connect()
    
    # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
    inverted_index = {}
    
    # Get all posts content
    posts = await get_all_posts(prisma_client).values_list("id", "content")
        
    # Tokenize the content + Map the content to the post_id
    
    # Create the Postinglists
    for post in posts:
        words = post[1].split()
        for word in words:
            if word in inverted_index:
                inverted_index[word].insertSorted(post[0])
            else:
                inverted_index[word] = LinkedList(post[0])
    
    await prisma_client.disconnect()