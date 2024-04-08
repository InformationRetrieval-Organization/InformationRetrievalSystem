# TODO: Implement the Vector Space Model, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/4
import math
from db.processed_posts import get_all_processed_posts
from boolean_model import _inverted_index
from preprocessing import get_all_processed_posts


def search_vector_space(query):
    
    return query

async def build_vector_space_model():

    posts = await get_all_processed_posts()

    posts = [(post.id, post.content) for post in posts]

    vocabulary = get_all_processed_posts

    # Step 2: Calculate the document frequency (DF) for each term
    document_frequency = {}
    for term in vocabulary:
        document_frequency[term] = len(_inverted_index[term])

    # Step 3: Calculate the inverse document frequency (IDF) for each term
    total_documents = len(posts)
    inverse_document_frequency = {}
    for term, df in document_frequency.items():
        inverse_document_frequency[term] = compute_inverse_document_frequency(total_documents, df)

    global _term_document_weight_matrix
    for post in posts:
        #every post has its own vector creating this vector
        tfidf_vector = []
        for term in vocabulary:
            term_count = post.lower().count(term)
            tf = compute_sublinear_tf_scaling(term_count)
            idf = inverse_document_frequency[term]
            tfidf = compute_tf_idf_weighting(tf,idf)
            tfidf_vector.append(tfidf)
        _term_document_weight_matrix.append(tfidf_vector)

    return None

def compute_inverse_document_frequency(N, df):
    return math.log2(N/df)

def compute_tf_idf_weighting(tf, idf):
    return tf * idf

def compute_sublinear_tf_scaling(tf):
    return 1 + math.log(tf) 