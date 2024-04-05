# TODO: Implement the Boolean Model, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/3

from sklearn.feature_extraction.text import TfidfVectorizer
from prisma import Prisma
from db.posts import get_all_posts, create_post
from information_retrieval.linked_list import LinkedList

inverted_index = {} # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
term_frequency = {} # Store the term frequency of each word

async def build_boolean_model():
    prisma_client = Prisma()
    await prisma_client.connect()
    
    global inverted_index
    global term_frequency 
    
    # Get all posts content
    posts = await get_all_posts(prisma_client).values_list("id", "content")

    # Create the Postinglists and map the term frequency
    for post in posts:
        words = post[1].split()
        for word in words:
            if word in inverted_index:
                inverted_index[word].insertSorted(post[0])
                term_frequency[word] += 1
            else:
                inverted_index[word] = LinkedList(post[0])
                term_frequency[word] = 1
    
    await prisma_client.disconnect()
    
def search_boolean_model(query):
    
    # For testing purposes, should be removed later
    words = [entry[1] for entry in query]
    term_frequency[words[0]] = 10 
    term_frequency[words[1]] = 30
    term_frequency[words[2]] = 2
    term_frequency[words[3]] = 5
    
    # First search tokens by frequency
    sorted_query = sorted(query, key=lambda word: term_frequency[word[1]])
    
    for entry in sorted_query:
        # ToDo implement search logic here
        # Look through the inverted index and find the post_ids that contain the word
        # store the post_ids in a list
        # Then perform the boolean operation on the list
        print(entry[0], entry[1])
    return sorted_query