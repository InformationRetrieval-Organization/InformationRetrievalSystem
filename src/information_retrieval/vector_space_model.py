# TODO: Implement the Vector Space Model, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/4
import math
from db.processed_posts import get_all_processed_posts
import information_retrieval.globals
import information_retrieval.linked_list
import numpy as np


async def search_vector_space(query):
    posts = await get_all_processed_posts()
    posts = [(post.id, post.content) for post in posts]

    # Step 2: Calculate the document frequency (DF) for each term
    total_documents = len(posts)
    inverse_document_frequency = {}
    query_weight_matrix = []

    for term in information_retrieval.globals._vocabulary:
        df = information_retrieval.globals._inverted_index[term].length()
        # Step 3: Calculate the inverse document frequency (IDF) for each term
        inverse_document_frequency[term] = compute_inverse_document_frequency(total_documents, df)
 
    #every post has its own vector creating this vector
    tfidf_vector = [compute_tf_idf_weighting(compute_sublinear_tf_scaling(query.count(term)), inverse_document_frequency[term]) for term in information_retrieval.globals._vocabulary]
    query_weight_matrix = tfidf_vector

    doc_cosine_similiarity_map = {}

    for doc_id, vector in information_retrieval.globals._document_id_vector_map.items():
        dot_product = np.dot(query_weight_matrix, vector)
        magnitude_query = np.linalg.norm(query_weight_matrix)
        magnitude_entry = np.linalg.norm(vector)
        cosine_similarity = dot_product / (magnitude_query * magnitude_entry)
        doc_cosine_similiarity_map[doc_id] = cosine_similarity
    sorted_docs = sorted(doc_cosine_similiarity_map.items(), key=lambda x: x[1], reverse=True)

    # Extract the sorted document IDs into a list
    sorted_doc_ids = [doc_id for doc_id, _ in sorted_docs]
    
    return sorted_doc_ids

async def build_vector_space_model():
    """
    Build the Vector Space Model
    """
    vocabulary = information_retrieval.globals._vocabulary
    
    print("Building Vector Space Model")
        
    posts = await get_all_processed_posts()
    posts = [(post.id, post.content) for post in posts]

    # Step 2: Calculate the document frequency (DF) for each term
    total_documents = len(posts)
    inverse_document_frequency = {}
    for term in vocabulary:
        df = information_retrieval.globals._inverted_index[term].length()
        # Step 3: Calculate the inverse document frequency (IDF) for each term
        inverse_document_frequency[term] = compute_inverse_document_frequency(total_documents, df)

    for post in posts:
        #every post has its own vector creating this vector
        tfidf_vector = [compute_tf_idf_weighting(compute_sublinear_tf_scaling(post[1].count(term)), inverse_document_frequency[term]) for term in vocabulary]
        information_retrieval.globals._term_document_weight_matrix.append(tfidf_vector)
        information_retrieval.globals._document_id_vector_map[post[0]] = tfidf_vector 
    print("Vector Space Model Built")
    return None

def compute_inverse_document_frequency(N, df):
    return math.log2(N/df)

def compute_tf_idf_weighting(tf, idf):
    return tf * idf

def compute_sublinear_tf_scaling(tf):
    if tf > 0:
        return 1 + math.log(tf) 
    return 0