# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/3

from sklearn.feature_extraction.text import TfidfVectorizer
from db.posts import get_all_posts, create_post
from information_retrieval.linked_list import LinkedList

_inverted_index = {} # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
_term_frequency = {} # Store the term frequency of each word
_all_doc_ids = set() # Store all the document ids

async def build_boolean_model():
    global _inverted_index
    global _term_frequency 
    
    # Get all posts content
    posts = await get_all_posts()
    posts = [(post.id, post.content) for post in posts]

    # Create the Postinglists and map the term frequency
    for post in posts:
        words = post[1].split()
        _all_doc_ids.add(post[0])
        for word in words:
            if word in _inverted_index:
                _inverted_index[word].insertSorted(post[0])
                _term_frequency[word] += 1
            else:
                _inverted_index[word] = LinkedList(post[0])
                _term_frequency[word] = 1
    
def search_boolean_model(query):
    global _all_doc_ids
    id_set = set(_all_doc_ids)
    
    # First sort tokens by frequency
    try:
        sorted_query = sorted(query, key=lambda word: _term_frequency[word[1]])
    except KeyError:
        sorted_query = query
    
    for entry in sorted_query:
        # Call different functions based on the operator
        if entry[0] == "AND":
            id_set = _and_processing(entry[1], id_set)
        elif entry[0] == "OR": 
            id_set = _or_processing(entry[1], id_set)
        elif entry[0] == "NOT":
            id_set = _not_processing(entry[1], id_set)
            
    return list(id_set)

def _and_processing(word, id_set):
    try:
        ids_of_index = set(_inverted_index[word])
        id_set = id_set.intersection(ids_of_index)
    except KeyError:
        id_set = set() # If the word is not in the index, then the result is empty
    return id_set

def _or_processing(word, id_set):
    try:
        ids_of_index = set(_inverted_index[word])
        id_set = id_set.union(ids_of_index)
    except KeyError:
        pass   # If the word is not in the index, it is not necessary to add it
    return id_set

def _not_processing(word, id_set):
    try:
        ids_of_index = set(_inverted_index[word])
        id_set = id_set.difference(ids_of_index)
    except KeyError:
        pass    # If the word is not in the index, it is not necessary to remove it
    return id_set
