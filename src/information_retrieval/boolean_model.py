# TODO: Implement the Boolean Model, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/3

from sklearn.feature_extraction.text import TfidfVectorizer
from prisma import Prisma
from db.posts import get_all_posts, create_post
from information_retrieval.linked_list import LinkedList

_inverted_index = {} # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
_term_frequency = {} # Store the term frequency of each word
_all_doc_ids = {} # Store all the document ids

async def build_boolean_model():
    prisma_client = Prisma()
    await prisma_client.connect()
    
    global _inverted_index
    global _term_frequency 
    
    # Get all posts content
    posts = await get_all_posts(prisma_client).values_list("id", "content")

    # Create the Postinglists and map the term frequency
    for post in posts:
        words = post[1].split()
        for word in words:
            if word in _inverted_index:
                _inverted_index[word].insertSorted(post[0])
                _term_frequency[word] += 1
            else:
                _inverted_index[word] = LinkedList(post[0])
                _term_frequency[word] = 1
                _all_doc_ids.add(post[0])
    
    await prisma_client.disconnect()
    
def search_boolean_model(query):
    id_set = _all_doc_ids.copy()
    
    """
    # For testing purposes, should be removed later
    words = [entry[1] for entry in query]
    _term_frequency[words[0]] = 10 
    _term_frequency[words[1]] = 30
    _term_frequency[words[2]] = 2
    _term_frequency[words[3]] = 5
    """
    
    # First search tokens by frequency
    sorted_query = sorted(query, key=lambda word: _term_frequency[word[1]])
    
    for entry in sorted_query:
        # Call different functions based on the operator
        if entry[0] == "AND":
            id_set = _and_processing(entry[1], id_set)
        elif entry[0] == "OR": 
            id_set = _or_processing(entry[1], id_set)
        elif entry[0] == "NOT":
            id_set = _not_processing(entry[1], id_set)

        print(entry[0], entry[1])
        
    return id_set

def _and_processing(word, id_set):
    ids_of_index = _inverted_index[word]
    id_set = id_set.intersection(ids_of_index)
    return id_set

def _or_processing(word, id_set):
    ids_of_index = _inverted_index[word]
    id_set = id_set.union(ids_of_index)
    return id_set

def _not_processing(word, id_set):
    ids_of_index = _inverted_index[word]
    id_set = id_set.difference(ids_of_index)
    return id_set