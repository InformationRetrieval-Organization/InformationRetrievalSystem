# TODO: Implement SVD (single value decomposition) in the vector space model to handle synonyms f.e.
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/9
import math
from typing import List
from db.processed_posts import get_all_processed_posts
import information_retrieval.globals
import information_retrieval.linked_list
import numpy as np


async def search_vector_space_model(query: List[str]) -> List[int]: 
    """
    Creates the Queryvector and calculates the cosine similiarity between the Queryvector and the Documentvectors
    """
    # Get all processed Posts to 
    posts = await get_all_processed_posts()
    posts = [(post.id, post.content) for post in posts]

    # Calculate the document frequency (DF) for each term
    total_documents = len(posts)
    inverse_document_frequency = {}
    # Matrix dimension 1x1
    query_weight_matrix = []

    for term in information_retrieval.globals._vocabulary:
        df = information_retrieval.globals._inverted_index[term].length()
        # Calculate the inverse document frequency (IDF) for each term
        inverse_document_frequency[term] = compute_inverse_document_frequency(total_documents, df)
 
    # Every post has its own vector which is created below
    tfidf_vector = [compute_tf_idf_weighting(compute_sublinear_tf_scaling(query.count(term)), inverse_document_frequency[term]) for term in information_retrieval.globals._vocabulary]
    query_weight_matrix = tfidf_vector
    # Map each document by id to the corressponding cosine similiarity
    doc_cosine_similiarity_map = {}

    for doc_id, vector in information_retrieval.globals._document_id_vector_map.items():
        # Calculate the Cosine similiarity by using the numpy library
        # Calculating the dot product between the Queryvector and the Documentvector
        dot_product = np.dot(query_weight_matrix, vector)
        # Calculate the norms for the Queryvector and the Documentvector
        magnitude_query = np.linalg.norm(query_weight_matrix)
        magnitude_entry = np.linalg.norm(vector)
        # Calculating the Cosine similiarity
        cosine_similarity = dot_product / (magnitude_query * magnitude_entry)
        # multiply cosine similarity with the date coefficient
        cosine_similarity *= information_retrieval.globals._date_coefficient[doc_id]
        # Adding the Results to the map created before
        doc_cosine_similiarity_map[doc_id] = cosine_similarity 
    # Sort the map by the highest cosine similiarity, lambda takes the second index in the tuple and used these to sort
    sorted_docs = sorted(doc_cosine_similiarity_map.items(), key=lambda x: x[1], reverse=True)
    # Extract the sorted document IDs into a list
    # In this contex "_" is a placeholder, we are not interested in it so we use this convention
    sorted_doc_ids = [doc_id for doc_id, _ in sorted_docs if _ > 0.0]
    return sorted_doc_ids

async def build_vector_space_model():
    """
    Build the Vector Space Model
    """
    vocabulary: List[str] = information_retrieval.globals._vocabulary
    
    print("Building Vector Space Model")
        
    posts = await get_all_processed_posts()
    posts = [(post.id, post.content) for post in posts]

    # Calculate the document frequency (DF) for each term
    total_documents = len(posts)
    inverse_document_frequency = {}

    for term in vocabulary:
        # Calculate the df it is the length of the linked list of occurance documents for a particular term
        df : int = information_retrieval.globals._inverted_index[term].length()
        # Calculate the inverse document frequency (IDF) for each term
        inverse_document_frequency[term] = compute_inverse_document_frequency(total_documents, df)

    for post in posts:
        # Every post has its own vector these are created below and added in the corresponding maps
        tfidf_vector = [compute_tf_idf_weighting(compute_sublinear_tf_scaling(post[1].count(term)), inverse_document_frequency[term]) for term in vocabulary]
        # Matrix dimension is term x documents
        information_retrieval.globals._term_document_weight_matrix.append(tfidf_vector)
        information_retrieval.globals._document_id_vector_map[post[0]] = tfidf_vector 

    print("Vector Space Model Built")
    return None

def compute_inverse_document_frequency(N : int, df: int) -> float:
    return math.log2(N/df)

def compute_tf_idf_weighting(tf: float, idf: float) -> float:
    return tf * idf

def compute_sublinear_tf_scaling(tf: int) -> float:
    if tf > 0:
        return 1 + math.log(tf) 
    return 0